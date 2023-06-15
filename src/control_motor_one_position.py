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


#xx = [i/1 for i in range(175)]
def plot_two_function(title, y1_1, y1_2, y2_1, y2_2, t, color1, color2, label1, label2, label3):
    plt.figure(figsize=(15,15))
    
    plt.subplot(2, 1, 1)
    plt.grid()
    plt.plot(t, y1_1, color = color1, label = label1, linestyle = 'dashdot', linewidth = 3.5)
    plt.plot(t, y1_2, color = color2, label = label2, linewidth = 1.5)
    plt.ylabel("Inclinación (grados)")
    plt.title(title)
    plt.legend()
    
    plt.subplot(2, 1, 2)
    plt.grid()
    plt.xlabel("Tiempo (segundos)")
    plt.ylabel("Orientación (grados)")
    plt.plot(t, y2_1, color = color1, label = label1, linestyle = 'dashdot', linewidth = 3.5)
    plt.plot(t, y2_2, color = color2, label = label3, linewidth = 1.5)
    plt.legend()
    plt.savefig('MLP_v7_II_prueba.png')
    return plt.show()


# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1, 2, 3])  # motor's ids
motors.startMotors()  # start motors

# Sensor
mi_sensor = Sensor()
mi_sensor.sensorStream()

# Trget values
incli_target = 10
orient_target = 15

# Instantiate InverseKinematics class
kine1 = InverseKinematics(incli_target, orient_target)
theta1, theta2, theta3 = kine1.neckInverseKinematics()  # saving the length's cables

motors.setupPositionsMode(12,12)
motors.setPositions([theta1, theta2, theta3])

# Kowing the sensor lecture after setting the IK position
#ik_incli, ik_orient = mi_sensor.readSensor(mi_sensor)

# Model trained
model_reg = joblib.load('/home/sofia/SOFIA_Python/ml/TFM/trained_error_motors_MASTER_V7.pkl')

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


#while (time < 20):
for step in np.arange(0,12,0.05):
    step =+ step
    #print(step)
    ik_incli, ik_orient = mi_sensor.readSensor(mi_sensor)

    # Calculate the Inclination and Orientation sensor error
    error_i = incli_target - ik_incli 
    error_o = orient_target - ik_orient

    # Just to compare the final values of theta (para saber si los valores de la prediccion están bien)
    #incli_rect = ik_incli + error_i 
    #orient_rect = ik_orient + error_o
    incli_rect = incli_target + error_i
    orient_rect = orient_target #+ error_o
    #if error_o<= 90:
    #    orient_rect = orient_target + error_o

    kine2 = InverseKinematics(incli_rect, orient_rect)
    theta_rect1, theta_rect2, theta_rect3 = kine2.neckInverseKinematics() 

    # Obtain the predictions from the model, that are the 3 values of theta 
    scaler = Normalizer()

    values_to_predict = np.array([incli_target, orient_target, error_i, error_o]).reshape(-1,1)
    #values_to_predict_trans = [[math.radians(i) for i in values_to_predict]]
    values_to_predict_trans = StandardScaler().fit_transform(values_to_predict)
    values_to_predict_trans_ad = (values_to_predict_trans * std_motors + mean_motors).reshape(1,-1)
    #values_to_predict = values_to_predict.flatten()
    pred = model_reg.predict(values_to_predict_trans_ad)
    pred = pred.flatten().tolist()

    error_theta1 = pred[0] # Grab the values of theta for each motor
    error_theta2 = pred[1]
    error_theta3 = pred[2]
    
    new_theta1 = theta_rect1 + error_theta1 # Adjusting theta (IK theta_rect + prediction error)
    new_theta2 = theta_rect2 + error_theta2
    new_theta3 = theta_rect3 + error_theta3

        #print sensor
    print("Inclination: ", round(ik_incli, 1),
            " Orientation: ", round(ik_orient, 1))

    print('Rect. incli: ' , round(incli_rect,1), '  Rect. orient:', round(orient_rect,1))
        
    # Setting new positions with the adjusted thetas
    motors.setPositions([new_theta1, new_theta2, new_theta3])

    # Reading sensor again
    #ik_incli, ik_orient = mi_sensor.readSensor(mi_sensor)
    end_time = timer() # record t+ error_ohe time again
    elapsed_time = end_time - start_time # calculate the elapsed time
    print(f"Tiempo: {elapsed_time:.2f} secondos")  # print the elapsed time in seconds with 6 decimal places


    incli_data.append(ik_incli)
    orient_data.append(ik_orient)

    list_incli_target.append(incli_target)
    list_orient_target.append(orient_target)

    time_data.append(elapsed_time)




plot_two_function("Control de lazo cerrado de la Cinemática Inversa - MLP datos ajustados a la recta",
                 list_incli_target,incli_data,list_orient_target,orient_data, time_data,
                 "black", "#FFC30F", 
                 "Referencia","Inclinación - CI","Orientación - CI")

motors.setPositions([0,0,0])

'''y_axis_i = incli_data
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


