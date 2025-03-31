
import math
import numpy as np
import pandas as pd


from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
from model.sensor import Sensor


# Motors
motors = SystemMotors(2)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1,2], "SoftClawMotorConfig.json")  # motor's ids
motors.startMotors()  # start motors

# Sensor
#mi_sensor = Sensor()  # instantiate Sensor class
#mi_sensor.sensorStream()  # enable sensor
# Parameters of the DataFrame
# Initial positions
orientation = 0
inclination = 0

# Parameters of the DataFrameo
cols = ['I', 'O', 'M1', 'M2']
data = []
motors.setupPositionsMode(2, 2)  # setting velocity and acceleration values

# Inclination's repetition
#motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
#motors.loadMotors([1, 2, 3])  # motor's ids
#motors.startMotors()  # start m
for inclination in range(5, 30, 10):
    # Orientation's repetition
    for orientation in range(5, 120, 1):
        # instantiate InverseKinematics class
        kine1 = InverseKinematics(inclination, orientation)
        theta1, theta2 = kine1.clawInverseKinematics()  # saving the length's cables

        motors.setPositions([theta1, theta2])

        # Knowing the Inclination and Orientation of the sensor, with a previous motor position
        for i in np.arange(0, 1):  # time sampling >> steps of 0.02
            #incli, orient = mi_sensor.readSensorArm(mi_sensor)

            print("Inclination: ", round(inclination, 1),
                  " Orientation: ", round(orientation, 1))

            # Adding the values of incli, orient and encoders in "data"
            data.append([inclination, orientation, motors.motorsArray[0].getPosition(
            ), motors.motorsArray[1].getPosition()])

    # adding the data values (array type), to the data frame
    df = pd.DataFrame(data, columns=cols)
    # print(df)
    df.to_csv(
        '/home/sofia/SOFIA_Python/data/Data_2025/claw_trajectory.csv', index=False)
    # df.to_csv(
        #'/home/sofia/SOFIA_Python/data/Data_2023/dataSOFIA_Python_february/data_orient10_MASTER_24.csv', index=False)
    df.info()

    print("Inclination: ", round(inclination, 1), " Orientation: ", round(orientation, 1))

print("Data Ready")
motors.setPositions([0,0])