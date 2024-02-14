
import math
import numpy as np
import pandas as pd
from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
from model.sensor import Sensor
import time
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
cols = ['Inclination', 'Orientation', 'M1', 'M2', 'M3','Peso']
data = []
motors.setupPositionsMode(12, 12)  # setting velocity and acceleration values

# instantiate SystemMotors class >> number of motors
#motors.loadMotors([1, 2, 3])  # motor's ids

motors.startMotors()  # start m

#Define time parameters
sampling_time = 0.03  # Sampling time in seconds
total_time = 25  # Total time for each iteration in seconds
data_collection_time = 9  # Time for data collection in seconds

# Motors setup
motors.setupPositionsMode(12, 12)  # Setting velocity and acceleration values
motors.startMotors()  # Start motors

for inclination in range(5, 41, 5):
    # Orientation's repetition
    for orientation in range(5, 361, 10):
        # instantiate InverseKinematics class
        kine1 = InverseKinematics(inclination, orientation)
        theta1, theta2, theta3 = kine1.neckInverseKinematics()  # saving the length's cables

        motors.setPositions([theta1, theta2, theta3])

        start_time = time.time()  # Start the timer

        # Data collection loop
        while (time.time() - start_time) < total_time:
            incli, orient = mi_sensor.readSensor(mi_sensor)

            if (time.time() - start_time) >= (total_time - data_collection_time):
                print("Inclination: ", round(incli, 1),
                      " Orientation: ", round(orient, 1))

                # Adding the values of incli, orient, and encoders to "data"
                data.append([incli, orient, motors.motorsArray[0].getPosition(),
                             motors.motorsArray[1].getPosition(), motors.motorsArray[2].getPosition(), 1000])

            time.sleep(sampling_time)

    # Add collected data to DataFrame
    df = pd.DataFrame(data, columns=cols)
    df.to_csv('/home/sofia/SOFIA_Python/data/Data_prueba_alba/test_peso1000.csv', index=False)

    df.info()
    print("Inclination: ", round(incli, 1), " Orientation: ", round(orient, 1))
