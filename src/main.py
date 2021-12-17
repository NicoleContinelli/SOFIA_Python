
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

# Initial positions
orientation = 0
inclination = 0

# Parameters of the DataFrame
cols = ['Inclination', 'Orientation', 'M1', 'M2', 'M3']
data = []
motors.setupPositionsMode(12, 12) # setting velocity and acceleration values
# Inclination's repetition
for inclination in range(5, 51, 5):
    #for i in range(10, 31, 10):
# Orientation's repetition
    for orientation in range(5, 360, 10):
        kine1 = InverseKinematics(inclination, orientation)  # instantiate InverseKinematics class
        theta1, theta2, theta3 = kine1.neckInverseKinematics()  # saving the length's cables

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

            #print("Inclination: ", round(incli, 1), " Orientation: ", round(orient, 1))

            # Adding the values of incli, orient and encoders in "data"
            data.append([incli, orient, motors.motorsArray[0].getPosition(), motors.motorsArray[1].getPosition(), motors.motorsArray[2].getPosition()])
    df = pd.DataFrame(data, columns = cols)  # adding the data values (array type), to the data frame
    #print(df)
    df.to_csv('/home/humasoft/SOFIA_Python/data/data_december/data_orient10_peso500_izquierda.csv', index = False)
    df.info()
            
    #print("Inclination: ", round(incli, 1), " Orientation: ", round(orient, 1))

print("Data Ready")
