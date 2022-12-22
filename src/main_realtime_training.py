import math
import numpy as np
import pandas as pd
import joblib
import time

from model.system_motors import SystemMotors
from model.sensor import Sensor
from model.data_collection import DataCollection


# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([2, 3, 1])  # motor's ids
motors.startMotors()  # start motors

# Sensor
mi_sensor = Sensor()  # instantiate Sensor class
mi_sensor.sensorStream()  # enable sensor

# Parameters of the DataFrame
data = []
cols = ['Inclination', 'Orientation', 'M1', 'M2', 'M3']
data_col = DataCollection()  # instantiate DataCollection class
motors.setupPositionsMode(12, 12)  # setting velocity and acceleration values

# Load the data with the predicted values
data_pred = pd.read_csv(
    '/home/humasoft/SOFIA_Python/ml/predicted_data_ANN_3files_optparams.csv')

# ML
model_reg = joblib.load('/home/humasoft/trained_model_reg_optiparam.pkl')

# Target Values
inclination = int(input("Digit inclination: "))
orientation = int(input("Digit orientation: "))
error_i = 5
error_o = 5


# in angles
while (np.abs(error_i) > 0.8 or np.abs(error_o) > 7.2):
    # calling data_neck_sensor function (passing fromr radians to degrees)
    sensor_data = data_col.data_neck_sensor(mi_sensor)
    sensor_data_final = list(sensor_data)  # converting a tuple to list
    print(sensor_data_final)
    error_i = (inclination - sensor_data_final[0])
    sensor_data_final[0] += error_i

    error_o = (orientation - sensor_data_final[1])
    sensor_data_final[1] += error_o


    pred = model_reg.predict([[sensor_data_final[0], sensor_data_final[1]]])
    thetas = pred.flatten().tolist()

    motors.setPositions([thetas[0], thetas[1], thetas[2]])

    # calling data_neck_motors function (collecting the encoders values)
    motor_data = data_col.data_neck_motors(motors)
    motor_data_final = list(motor_data)  # converting a tuple to list

    data.append([sensor_data_final[0],
                 sensor_data_final[1],
                 motor_data_final[0],
                 motor_data_final[1],
                 motor_data_final[2]])

    # adding the data values (array type), to the data frame
    df = pd.DataFrame(data, columns=cols)
    df.to_csv(
        '/home/humasoft/SOFIA_Python/data/data_february/data_ANN_3files_optparams_control.csv', index=False)
        
print("Data Ready")
