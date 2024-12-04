from model.sensor import Sensor
from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
import math
import numpy as np
import pandas as pd
import time 

# Knowing the Inclination and Orientation of the sensor, with a prevoius motor position

# Motors
#motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
#motors.loadMotors([31, 32, 33], "SoftArmMotorConfig.json")  # motor's ids
#motors.startMotors()  # start motors

# Sensor
mi_sensor = Sensor()
mi_sensor.sensorStream()

#kine1 = InverseKinematics(10, 90)  # instantiate InverseKinematics class
#theta1, theta2, theta3 = kine1.armInverseKinematics()  # saving the length's cables

#print("Sleeping time!!!", time.sleep(3))
#motors.setupPositionsMode(3,3)
#print("Sleeping time!!!", time.sleep(3))

#motors.setPositions([theta1, theta2, theta3])

for i in np.arange(0, 100, 0.02):
    inclination, orientation = mi_sensor.readSensorArm(
        mi_sensor)  # new method of teh sensor class

    print("Inclination: ", round(inclination, 1),
          " Orientation: ", round(orientation, 1))
    
'''     print("Roll: ", roll,
          " Pitch: ", pitch, 
            "yaw: ", yaw)'''
