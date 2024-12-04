from model.sensor import Sensor
from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
import math
import numpy as np
import pandas as pd
import time 

# Knowing the Inclination and Orientation of the sensor, with a prevoius motor position

# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motorsssss
motors.loadMotors([31, 32, 33], "SoftArmMotorConfig.json")  # motor's ids
motors.startMotors()  # start motors

# Sensor
mi_sensor = Sensor()
mi_sensor.sensorStream()

kine1 = InverseKinematics(39, 60)  # instantiate InverseKinematics class
theta1, theta2, theta3 = kine1.armInverseKinematics3()  # saving the length's cables

print("Sleeping time!!!", time.sleep(1))
motors.setupPositionsMode(3,3)
print("Sleeping time!!!", time.sleep(1))


print("Thetas:", theta1, theta2, theta3)
x = input('Enter YES to continue')
print('Starting program... ' + x) 

motors.setPositions([theta1, theta2, theta3])


for i in np.arange(0, 10, 0.02):
    inclination, orientation = mi_sensor.readSensorArm(mi_sensor)  # new method of the sensor class

    print("Inclination: ", round(inclination, 1),
          " Orientation: ", round(orientation, 1))
    
motors.setPositions([0,0,0])
