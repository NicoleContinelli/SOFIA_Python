
import math
import numpy as np
import pandas as pd

'''
from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
from model.sensor import Sensor

# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1, 2, 3])  # motor's ids
motors.startMotors()  # start motors

# Sensor
mi_sensor = Sensor()  # instantiate Sensor class
mi_sensor.sensorStream()  # enable sensor

'''

data_ANN = pd.read_csv('/home/humasoft/SOFIA_Python/ml/predicted_data_ANN.csv')

for inclination in range(len(data_ANN)):
    if data_ANN['I'].values() == 40:
        print(data_ANN.iloc[inclination,0])





