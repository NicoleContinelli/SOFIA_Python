from model.sensor import Sensor
from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
import math
import numpy as np
import pandas as pd
import joblib


import matplotlib.pyplot as plt


# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1, 2, 3])  # motor's ids
motors.startMotors()  # start motors

# Sensor
mi_sensor = Sensor()
mi_sensor.sensorStream()

# Trget values
incli_target = 33
orient_target = 200

# Instantiate InverseKinematics class
kine1 = InverseKinematics(incli_target, orient_target)
theta1, theta2, theta3 = kine1.neckInverseKinematics()  # saving the length's cables

motors.setupPositionsMode(12, 12)
motors.setPositions([theta1, theta2, theta3])

# Kowing the sensor lecture after setting the IK position
ik_incli, ik_orient = mi_sensor.readSensor(mi_sensor)

# Model trained
model_reg = joblib.load('/home/sofia/SOFIA_Python/ml/TFM/trained_error_motors_MASTER_V1.pkl')

# For plotting the graph
incli_data = []
orient_data = []

#while (time < 20):
for time in np.arange(0,15,0.02):
    time =+ time
    print(time)
    # Calculate the Inclination and Orientation sensor error
    error_i = incli_target - ik_incli
    error_o = orient_target - ik_orient

    # Just to compare the final values of theta (para saber si los valores de la prediccion están bien)
    incli_rect = ik_incli + error_i
    orient_rect = ik_orient + error_o

    kine2 = InverseKinematics(incli_rect, orient_rect)
    theta_rect1, theta_rect2, theta_rect3 = kine2.neckInverseKinematics() 

    # Obtain the predictions from the model, that are the 3 values of theta 
    pred = model_reg.predict([[incli_target, orient_target, error_i, error_o]])
    pred = pred.flatten().tolist()

    error_theta1 = pred[0] # Grab the values of theta for each motor
    error_theta2 = pred[1]
    error_theta3 = pred[2]
    
    new_theta1 = theta_rect1 + error_theta1 # Adjusting theta (IK theta + prediction error)
    new_theta2 = theta_rect2 + error_theta1
    new_theta3 = theta_rect3 + error_theta1

    print('Predictions:', new_theta1, new_theta2, new_theta3)
    print('Inverse K.:', theta_rect1, theta_rect2, theta_rect3)
    
    # Setting new positions with the adjusted thetas
    motors.setPositions([new_theta1, new_theta2, new_theta3])

    # Reading sensor again
    ik_incli, ik_orient = mi_sensor.readSensor(mi_sensor)
    incli_data.append(ik_incli)
    orient_data.append(ik_orient)

    print("Inclination: ", round(ik_incli, 1),
            " Orientation: ", round(ik_orient, 1))

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


'''print("error Inclination: ", round(incli_target - ik_incli, 1),
            " error Orientation: ", round(orient_target - ik_orient, 1))'''


