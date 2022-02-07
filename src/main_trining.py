import math
import numpy as np
import pandas as pd


from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
from model.sensor import Sensor


# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([2, 3, 1])  # motor's ids
motors.startMotors()  # start motors

# Sensor
mi_sensor = Sensor()  # instantiate Sensor class
mi_sensor.sensorStream()  # enable sensor

# Initial positions
orientation = 0
inclination = 0

# Parameters of the DataFrame
cols = ['Inclination', 'Orientation', 'M1', 'M2', 'M3']
data = []
motors.setupPositionsMode(12, 12) # setting velocity and acceleration values

#Load the data with the predicted values
data_pred = pd.read_csv('/home/humasoft/SOFIA_Python/ml/predicted_data_ANN_3files_optparams.csv')


# Inclination's repetition
for inclination in range(5, 41, 5):
   
# Orientation's repetition
    for orientation in range(5, 360, 10):

        row = data_pred[data_pred['I'] == inclination] [data_pred['O'] == orientation] #row with the predicted encoders
        
        # Set theta values >> looking for them in the "row" variable
        theta1 = row.iloc[0,2] 
        theta2 = row.iloc[0,3]
        theta3 = row.iloc[0,4]

        motors.setPositions([theta1, theta2, theta3])

        # Knowing the Inclination and Orientation of the sensor, with a previous motor position
        for i in np.arange(0, 2, 0.02):  # time sampling >> steps of 0.02
            pitch = mi_sensor.getPitch()
            roll = mi_sensor.getRoll()
            yaw = mi_sensor.getYaw()

            cos_p = math.cos(pitch)
            cos_r = math.cos(roll)
            sen_p = math.sin(pitch)
            sen_r = math.sin(roll)

            incli = math.sqrt(pitch**2 + roll**2) * (180 / math.pi)
            orient = ((math.atan2(roll, pitch) * (180 / math.pi)))

            # Conditions for having 360 degrees in orientation
            if orient > 0:
                orient = 359 - orient

            if orient < 0:
                orient = abs(orient)

            print("Inclination: ", round(incli, 1), " Orientation: ", round(orient, 1))

            # Adding the values of incli, orient and encoders in "data"
            data.append([incli, orient, motors.motorsArray[0].getPosition(), motors.motorsArray[1].getPosition(), motors.motorsArray[2].getPosition()])
    df = pd.DataFrame(data, columns = cols)  # adding the data values (array type), to the data frame
    #print(df)
    df.to_csv('/home/humasoft/SOFIA_Python/data/data_february/predicted_data_ANN_3files_optparams.csv', index = False)
    df.info()
            
    print("Inclination: ", round(incli, 1), " Orientation: ", round(orient, 1))

print("Data Ready")

