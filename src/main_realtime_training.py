import math
import numpy as np
import pandas as pd


from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
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
data_col = DataCollection() #instantiate DataCollection class
motors.setupPositionsMode(12, 12) # setting velocity and acceleration values

#Load the data with the predicted values
data_pred = pd.read_csv('/home/humasoft/SOFIA_Python/ml/predicted_data_ANN_3files_optparams.csv')


# Inclination's repetition
for inclination in range(5, 41, 10):
   
# Orientation's repetition
    for orientation in range(5, 360, 45):

        row = data_pred[data_pred['I'] == inclination] [data_pred['O'] == orientation] #row with the predicted encoders
        
        # Set theta values >> looking for them in the "row" variable
        theta1 = row.iloc[0,2] 
        theta2 = row.iloc[0,3]
        theta3 = row.iloc[0,4]

        motors.setPositions([theta1, theta2, theta3])

        # Knowing the Inclination and Orientation of the sensor, with a previous motor position
        for i in np.arange(0, 2, 0.02):  # Sampling time with steps of 0.02
            sensor_data = data_col.data_neck_sensor(mi_sensor) # calling data_neck_sensor function (passing fromr adians to degrees)
            sensor_data_final = list(sensor_data) # converting a tuple to list
            
            motor_data = data_col.data_neck_motors(motors) # calling data_neck_motors function (collecting the encoders values)
            motor_data_final = list(motor_data) # converting a tuple to list
            
            data.append([sensor_data_final[0], 
                         sensor_data_final[1], 
                         motor_data_final[0], 
                         motor_data_final[1], 
                         motor_data_final[2]])

    df = pd.DataFrame(data, columns = cols)  # adding the data values (array type), to the data frame
    df.to_csv('/home/humasoft/SOFIA_Python/data/data_february/predicted_data_ANN_3files_optparams.csv', index = False)
    #df.info() or print(df)
    

print("Data Ready")


