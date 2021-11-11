from Sensor import Sensor
from SystemMotors import SystemMotors
from InverseKinematics import InverseKinematics
import math
import numpy as np

# Knowing the Inclination and Orientation of the sensor, with a prevoius motor position

# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1, 2, 3])  # motor's ids
motors.startMotors()  # start motors

# Sensor
mi_sensor = Sensor()
mi_sensor.sensorStream()

kine1 = InverseKinematics(20, 90)  # instantiate InverseKinematics class
theta1, theta2, theta3 = kine1.neckInverseKinematics()  # saving the length's cables

motors.setupPositionsMode(10, 10)
# motors.setPositions([theta1, theta2, theta3])
motors.setPositions([2.17875967, -1.29508173, -0.60727285])

for i in np.arange(0, 30, 0.02):
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



#    print("Inclination: " + str(round(incli, 1)) + " Orientation: " + str(round(orient, 1)))
