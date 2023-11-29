
import math
import numpy as np
import pandas as pd


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
# Parameters of the DataFrame
# Initial positions
orientation = 0
inclination = 0

# Parameters of the DataFrame
cols = ['Inclination', 'Orientation', 'M1', 'M2', 'M3']
data = []
motors.setupPositionsMode(15, 15)  # setting velocity and acceleration values

# Inclination's repetition
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1, 2, 3])  # motor's ids
motors.startMotors()  # start m
for inclination in range(5, 41, 5):
    # Orientation's repetition
    for orientation in range(5, 361, 10):
        # instantiate InverseKinematics class
        kine1 = InverseKinematics(inclination, orientation)
        theta1, theta2, theta3 = kine1.neckInverseKinematics()  # saving the length's cables

        motors.setPositions([theta1, theta2, theta3])

        # Knowing the Inclination and Orientation of the sensor, with a previous motor position
        for i in np.arange(0, 2, 0.02):  # time sampling >> steps of 0.02
            incli, orient = mi_sensor.readSensor(mi_sensor)

            print("Inclination: ", round(incli, 1),
                  " Orientation: ", round(orient, 1))

            # Adding the values of incli, orient and encoders in "data"
            data.append([incli, orient, motors.motorsArray[0].getPosition(
            ), motors.motorsArray[1].getPosition(), motors.motorsArray[2].getPosition()])

    # adding the data values (array type), to the data frame
    df = pd.DataFrame(data, columns=cols)
    # print(df)
    df.to_csv(
        '/home/sofia/SOFIA_Python/data/Data_2023/dataSOFIA_Python_february/data_orient10_MASTER_24.csv', index=False)
    df.info()

    print("Inclination: ", round(incli, 1), " Orientation: ", round(orient, 1))

print("Data Ready")
