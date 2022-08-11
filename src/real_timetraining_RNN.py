import math
import numpy as np
import pandas as pd
import joblib  
import time

from model.system_motors import SystemMotors
from model.sensor import Sensor
from model.direct_kinematics import DirectKinematics
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
data_col = DataCollection() #instantiate DataCollection class
motors.setupPositionsMode(12, 12) # setting velocity and acceleration values

#Load the data with the predicted values
data_pred = pd.read_csv('/home/sofia/SOFIA_Python/ml/predicted_data_ANN_3files_optparams.csv')

#ML
model_reg = joblib.load('/home/sofia/trained_model_reg_optiparam.pkl')

#Target Values
inclination = int(input("Digit inclination: "))
orientation = int(input("Digit orientation: "))
error_i = 5
error_o = 5


pred = model_reg.predict([[inclination,orientation]])
thetas = pred.flatten().tolist()

motors.setPositions([thetas[0], thetas[1], thetas[2]])
#Sensor data
sensor_data = data_col.data_neck_sensor(mi_sensor) # calling data_neck_sensor function (passing from radians to degrees)
sensor_data_final = list(sensor_data)
#Motor data
motor_data = data_col.data_neck_motors(motors) # calling data_neck_motors function (collecting the encoders values)
motor_data_final = list(motor_data) # converting a tuple to list    

#RNN


#Error
dkine = DirectKinematics(th1, th2, th3)
dkine = list(dkine)
error_i = 0
error_o = 0
condition = True

#Do-while
while condition == True: 

    error_i = sensor_data_final[0] - dkine[0]
    error_o = sensor_data_final[1] - dkine[1]
    error = []

    error.extend(error_i, error_o)

    if (np.abs(error_i) > 0.8 or np.abs(error_o) > 7.2):
        condition = False


