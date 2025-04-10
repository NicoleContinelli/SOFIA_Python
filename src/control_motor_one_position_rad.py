from model.sensor import Sensor
from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics


import math
import numpy as np
import pandas as pd
import joblib


import matplotlib.pyplot as plt
from sklearn.preprocessing import Normalizer, StandardScaler

from timeit import default_timer as timer


#xx = [i/1 for i in range(2880)]
def plot_two_function(title, y1_1, y1_2, y2_1, y2_2, t, color1, color2, label1, label2, label3):
    plt.figure(figsize=(15,15))
    
    plt.subplot(2, 1, 1)
    plt.grid()
    plt.plot(t, y1_1, color = color1, label = label1, linestyle = 'dashdot', linewidth = 3.5)
    plt.plot(t, y1_2, color = color2, label = label2, linewidth = 1.5)
    plt.ylabel("Inclination (degrees)")
    plt.title(title)
    plt.legend()
    
    plt.subplot(2, 1, 2)
    plt.grid()
    plt.xlabel("Time (seconds)")
    plt.ylabel("Orientation (degrees)")
    plt.plot(t, y2_1, color = color1, label = label1, linestyle = 'dashdot', linewidth = 3.5)
    plt.plot(t, y2_2, color = color2, label = label3, linewidth = 1.5)
    plt.legend()
    #plt.savefig('MLP_v5_radianes.png')
    plt.savefig('MLP_paper_robot_one_pos_radians_v7.png')
    return plt.show()


# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1, 2, 3], "SoftNeckMotorConfig.json")  # motor's ids
motors.startMotors()  # start motors

# Sensor
mi_sensor = Sensor()
mi_sensor.sensorStream()

# Trget values
incli_target = 25
orient_target = 250

# Instantiate InverseKinematics class
kine1 = InverseKinematics(incli_target, orient_target)
theta1, theta2, theta3 = kine1.neckInverseKinematics()  # saving the length's cables

motors.setupPositionsMode(15,15)
motors.setPositions([theta1, theta2, theta3])

# Kowing the sensor lecture after setting the IK position
#ik_incli, ik_orient = mi_sensor.readSensor(mi_sensor)

# Model trained
model_reg = joblib.load('/home/sofia/SOFIA_Python/ml/TFM/trained_error_motors_MASTER_V6.pkl')

# For plotting the graph
incli_data = []
orient_data = []
time_data = []

# For plotting the graph - target values
list_incli_target = []
list_orient_target = []

start_time = timer()  # record the current time

# For normalizing the datatime_data.append(elapsed_time)
mean_motors = -0.045458604279763254
std_motors = 0.2670333006545897


#while (time < 20):
for step in np.arange(0,12,0.05):
    step =+ step
    print(step)
    ik_incli, ik_orient = mi_sensor.readSensorNeck(mi_sensor)

    # Calculate the Inclination and Orientation sensor error
    error_i = incli_target - ik_incli 
    error_o = orient_target - ik_orient

    # Just to compare the final values of theta (para saber si los valores de la prediccion están bien)
    #incli_rect = ik_incli + error_i 
    #orient_rect = ik_orient + error_o
    incli_rect = incli_target + error_i
    orient_rect = orient_target + error_o
    #if error_o<= 90:
        #orient_rect = orient_target + error_o

    kine2 = InverseKinematics(incli_rect, orient_rect)
    theta_rect1, theta_rect2, theta_rect3 = kine2.neckInverseKinematics() 

    # Obtain the predictions from the model, that are the 3 values of theta 
    scaler = Normalizer()

    values_to_predict = np.array([incli_target, orient_target, error_i, error_o])
    values_to_predict = values_to_predict.flatten()
    values_to_predict_trans = [[math.radians(i) for i in values_to_predict]]
    pred = model_reg.predict(values_to_predict_trans)
    pred = pred.flatten().tolist()

    error_theta1 = pred[0] # Grab the values of theta for each motor
    error_theta2 = pred[1]
    error_theta3 = pred[2]
    
    new_theta1 = theta_rect1 + error_theta1 # Adjusting theta (IK theta + prediction error)
    new_theta2 = theta_rect2 + error_theta2
    new_theta3 = theta_rect3 + error_theta3

            #print sensor
    '''print("Inclination: ", round(ik_incli, 1),
            " Orientation: ", round(ik_orient, 1))

    print('Rect. incli: ' , round(incli_rect,1), '  Rect. orient:', round(orient_rect,1))'''
    
    # Setting new positions with the adjusted thetas
    motors.setPositions([new_theta1, new_theta2, new_theta3])

    # Reading sensor again
    #ik_incli, ik_orient = mi_sensor.readSensor(mi_sensor)
    end_time = timer() # record the time again
    elapsed_time = end_time - start_time # calculate the elapsed time
    #print(f"Elapsed time: {elapsed_time:.6f} seconds")  # print the elapsed time in seconds with 6 decimal places


    incli_data.append(ik_incli)
    orient_data.append(ik_orient)

    list_incli_target.append(incli_target)
    list_orient_target.append(orient_target)

    #print sensor
    #print("Inclination: ", round(ik_incli, 1),
    #        " Orientation: ", round(ik_orient, 1))
    
    time_data.append(elapsed_time)

    data = {
    "Real Incli": incli_data,
    "Real Orient": orient_data,
    "Time": time_data,
    "Target Incli": list_incli_target,
    "Target Orient": list_orient_target 
    }

df = pd.DataFrame(data)
df.to_csv('/home/sofia/SOFIA_Python/data/Data_2025/Data_Paper_Robotics/one_pos_rad_v7.csv', index=False)

plot_two_function("Control de lazo cerrado de la Cinemática Inversa - MLP datos en escala de radianes",
                 list_incli_target,incli_data,list_orient_target,orient_data,time_data,
                 "black", "#FF5733", 
                 "Target","Inclination - IMU","Orientation - IMU")

motors.setPositions([0,0,0])
'''
plot_two_function("Control de lazo cerrado de la Cinemática Inversa  - MLP datos en escala de radianes",
                 list_incli_target,incli_data,list_orient_target,orient_data,time_data,
                 "black", "#FF5733", 
                 "Referencia","Inclinación - CI","Orientación - CI")

motors.setPositions([0,0,0])

y_axis_i = incli_data
y_axis_o = orient_data

fig, axs = plt.subplots(2)
axs[0].plot(y_axis_i, color='purple', label='Sensor Inclination')
axs[0].hlines(y=incli_target, xmin=0, xmax=len(y_axis_i), linewidth=1, color='black', linestyles='--', label='Target Inclination')
axs[0].set_title('Inclination Control')


axs[1].plot(y_axis_o, color='orange', label='Sensor Orientation')
axs[1].hlines(y=orient_target, xmin=0, xmax=len(y_axis_o), linewidth=1, color='black', linestyles='--', label='Target Orientation')
axs[1].set_title('Orientation Control')


axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Degrees')

axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Degrees')

axs[0].legend()
axs[1].legend()
plt.show()

motors.setPositions([0,0,0])

print("error Inclination: ", round(incli_target - ik_incli, 1),
            " error Orientation: ", round(orient_target - ik_orient, 1))'''


