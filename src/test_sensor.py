from model.sensor import Sensor
from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
import math
import numpy as np
import pandas as pd

# Knowing the Inclination and Orientation of the sensor, with a prevoius motor position

# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1, 2, 3])  # motor's ids
motors.startMotors()  # start motors

# Sensor
mi_sensor = Sensor()
mi_sensor.sensorStream()

kine1 = InverseKinematics(20, 0)  # instantiate InverseKinematics class
theta1, theta2, theta3 = kine1.neckInverseKinematics()  # saving the length's cables

motors.setupPositionsMode(12, 12) 
motors.setPositions([theta1, theta2, theta3])
#motors.setPositions([-0.91180212, -0.72023127,  2.07622717]) #I: 34 O: 126

# Parameters of the DataFrame
cols = ['Inclination', 'Orientation']
data = []

for i in np.arange(0, 3, 0.02):
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
        orient = orient

    if orient < 0:
        orient = 360 - abs(orient)

    print("Inclination: ", round(incli, 1), " Orientation: ", round(orient, 1))

'''
    # Adding the values of incli, orient and encoders in "data"
    data.append([incli, orient])


df = pd.DataFrame(data, columns = cols)  # adding the data values (array type), to the data frame
print(df)
df.to_csv(r'/home/humasoft/SOFIA_Python/Data/test_sensor_2-5s.csv', index = False)

'''
