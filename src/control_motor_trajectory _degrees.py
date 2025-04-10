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
import warnings
warnings.filterwarnings("ignore", message="X does not have valid feature names")


#xx = [i/1 for i in range(3200)]
def plot_two_function(title, t, y1_1, y1_2, y2_1, y2_2, color1, color2, label1, label2, label3):
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
    plt.savefig('MLP_paper_robot_trajectory_pos_degrees.png')
    #plt.savefig('MLP_V3_Trajectory_degrees.png')
    return plt.show()



# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1, 2, 3], "SoftNeckMotorConfig.json")  # motor's ids
motors.startMotors()  # start motors

# Sensor
mi_sensor = Sensor()
mi_sensor.sensorStream()

# Trget values - Initial positions
incli_target = 0
orient_target = 0

# Instantiate InverseKinematics class
kine1 = InverseKinematics(incli_target, orient_target)
theta1, theta2, theta3 = kine1.neckInverseKinematics()  # saving the length's cables

motors.setupPositionsMode(10, 10)
motors.setPositions([theta1, theta2, theta3])

# Kowing the sensor lecture after setting the IK position
ik_incli, ik_orient = mi_sensor.readSensorNeck(mi_sensor)

# Model trained
model_reg = joblib.load('/home/sofia/SOFIA_Python/ml/TFM/trained_error_motors_MASTER_V3.pkl')

# For plotting the graph
incli_data = []
orient_data = []
time_data = []


# For plotting the graph - target values
list_incli_target = []
list_orient_target = []

start_time = timer()  # record the current time

# For normalizing the data
mean_motors = -0.045458604279763254
std_motors = 0.2670333006545897

range_incli = range(40, 4, -10)

# Inclination's repetition
for incli_target in range_incli:
    # Orientation's repetition
    for orient_target in range(5, 361, 90):
        #while (time < 20):Control de lazo cerrado de la Cinemática Inversa  - MLP datos en escala de radianes
        for step in np.arange(0,10,0.05):
            step =+ step
            #print(step)
            ik_incli, ik_orient = mi_sensor.readSensorNeck(mi_sensor)

            # Calculate the Inclination and Orientation sensor error
            error_i = incli_target - ik_incli 
            error_o = orient_target - ik_orient

            # Just to compare the final values of theta (para saber si los valores de la prediccion están bien)
            #incli_rect = ik_incli + error_i 
            #orient_rect = ik_orient + error_o
            incli_rect = incli_target + error_i
            orient_rect = orient_target #+ error_o
            #if error_o<= 181:
                #orient_rect = orient_target + error_o

            kine2 = InverseKinematics(incli_rect, orient_rect)
            theta_rect1, theta_rect2, theta_rect3 = kine2.neckInverseKinematics() 

            # Obtain the predictions from the model, that are the 3 values of theta 
            scaler = Normalizer()

            values_to_predict = np.array([[incli_target, orient_target, error_i, error_o]])
            pred = model_reg.predict(values_to_predict)
            pred = pred.flatten().tolist()


            error_theta1 = pred[0] # Grab the values of theta for each motor
            error_theta2 = pred[1]
            error_theta3 = pred[2]
            
            new_theta1 = theta_rect1 + error_theta1 # Adjusting theta (IK theta_rect + prediction error)
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
            end_time = timer() # record t+ error_ohe time again
            elapsed_time = end_time - start_time # calculate the elapsed time
            #print(f"Tiempo: {elapsed_time:.2f} secondos")  # print the elapsed time in seconds with 6 decimal places


            incli_data.append(ik_incli)
            orient_data.append(ik_orient)

            list_incli_target.append(incli_target)
            list_orient_target.append(orient_target)

            time_data.append(elapsed_time)

data = {
    "Real Incli": incli_data,
    "Real Orient": orient_data,
    "Time": time_data,
    "Target Incli": list_incli_target,
    "Target Orient": list_orient_target 
    }

df = pd.DataFrame(data)
df.to_csv('/home/sofia/SOFIA_Python/data/Data_2025/Data_Paper_Robotics/trajectory_pos_degrees.csv', index=False)

plot_two_function("Control de trayectoria en lazo cerrado de la Cinemática Inversa - MLP sin transformación datos",time_data,
                 list_incli_target,incli_data,list_orient_target,orient_data,
                 "black", "#C70039", 
                 "Target","Inclination - IMU","Orientation - IMU")

motors.setPositions([0,0,0])

'''
plot_two_function("Control de trayectoria en lazo cerrado de la Cinemática Inversa - MLP sin transformación datos",time_data,
                 list_incli_target,incli_data,list_orient_target,orient_data,
                 "black", "#C70039", 
                 "Referencia","Inclinación - CI","Orientación - CI")

motors.setPositions([0,0,0])

y_axis_i = incli_data
y_axis_o = orient_data

fig, axs = plt.subplots(2)
axs[0].plot(y_axis_i, color='purple')
axs[0].set_title('Inclination Control')

axs[1].plot(y_axis_o, color='orange')
axs[1].set_title('Orientation Control')

plt.xlabel('Time (s)')
plt.ylabel('Degrees')
plt.show()


print("error Inclination: ", round(incli_target - ik_incli, 1),
            " error Orientation: ", round(orient_target - ik_orient, 1))'''


