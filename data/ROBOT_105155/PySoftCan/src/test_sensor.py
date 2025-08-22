from model.sensor import Sensor
from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
import math
import numpy as np
import pandas as pd

# Knowing the Inclination and Orientation of the sensor, with a prevoius motor position

# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1, 2, 3], "SoftNeckMotorConfig.json")  # motor's ids
motors.startMotors()  # start motors

# Sensor
mi_sensor = Sensor()
mi_sensor.sensorStream()

kine1 = InverseKinematics(0, 0)  # instantiate InverseKinematics class
theta1, theta2, theta3 = kine1.neckInverseKinematics()  # saving the length's cables

motors.setupPositionsMode(12, 12)
motors.setPositions([theta1, theta2, theta3])

for i in np.arange(0, 2, 0.02):
    inclination, orientation = mi_sensor.readSensorNeck(mi_sensor)  # new method of teh sensor class

    print("Inclination: ", round(inclination, 1),
          " Orientation: ", round(orientation, 1))
