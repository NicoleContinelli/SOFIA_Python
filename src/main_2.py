
import math
import numpy as np
import pandas as pd


from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
from model.sensor import Sensor


# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1, 2, 3], "SoftNeckMotorConfig.json")  # motor's ids
motors.startMotors()  # start motors

# Sensor
mi_sensor = Sensor()  # instantiate Sensor class
mi_sensor.sensorStream()  # enable sensor
# Parameters of the DataFrame
# Initial positions
orientation = 0
inclination = 0

# Parameters of the DataFrame
cols = ['Inclination', 'Orientation', 'M1', 'M2', 'M3']
data = []
#motors.setupPositionsMode(12, 12)  # setting velocity and acceleration values

# Inclination's repetition
#motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
#motors.loadMotors([1, 2, 3])  # motor's ids
#motors.startMotors()  # start m
for inclination in range(5, 36, 5):
    # Orientation's repetition
    for orientation in range(10, 361, 10):
        # instantiate InverseKinematics class
        kine1 = InverseKinematics(inclination, orientation)
        theta1, theta2, theta3 = kine1.neckInverseKinematics()  # saving the length's cables
        motors.setupPositionsMode(12, 12)  # setting velocity and acceleration values
        motors.setPositions([theta1, theta2, theta3])

        # Knowing the Inclination and Orientation of the sensor, with a previous motor position
        for i in np.arange(0, 2, 1):  # time sampling >> steps of 0.02
            incli, orient = mi_sensor.readSensorNeck(mi_sensor)

            print("Inclination: ", round(incli, 1),
                  " Orientation: ", round(orient, 1))


