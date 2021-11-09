# Sensors Libraries
import SerialComm as sc
import attitude_estimator as ae
import imu3dmgx510 as imu
import math
import numpy as np


from Motor import Motor
from SystemMotors import SystemMotors
from InverseKinematics import InverseKinematics
from Sensor import Sensor


# Motors movements with the classes
motors = SystemMotors(3)
print(motors.loadMotors([1,2,3]))
motors.startMotors()

mi_sensor = Sensor()
mi_sensor.sensorStream()


for pos in motors.getPositions():
    print(pos)

kine1 = InverseKinematics(0, 0)
theta1, theta2, theta3 = kine1.neckInverseKinematics()
print(theta1, theta2, theta3)

motors.setupPositionsMode(10, 10)
motors.setPositions([theta1, theta2, theta3])
#motors.motorsArray[2].getPosition()









'''
mi_sensor = imu.IMU3DMGX510("/dev/ttyUSB0", 50)
mi_sensor.set_streamon()
'''

'''

# Kinematics parameters
a = 0.052  # m distance between A and base
b = 0.052  # m distance between B and mobile platform
L0 = 0.107  # Neck Lenght



# mi_sensor.set_streamon() #>> para calibrar el sensor
'''
'''
for i in np.arange(0, 10, 0.02):
    print("Motor 1 = " + str(motor1.GetPosition()) + " Motor 2 = " + str(motor2.GetPosition()) + " Motor 3 = " + str(motor3.GetPosition()))
print(theta1, theta2, theta3)
'''



# Knowing the Inclination and Orientation of the sensor, with a prevoius motor position


for i in np.arange(0, 30, 0.02):
    pitch = mi_sensor.getPitch()
    roll = mi_sensor.getRoll()
    yaw = mi_sensor.getYaw()

    cos_p = math.cos(pitch)
    cos_r = math.cos(roll)
    sen_p = math.sin(pitch)
    sen_r = math.sin(roll)

#    print("Pitch:  ", round(pitch * (180 / math.pi), 2), "Roll:  ", round(roll * (180 / math.pi), 2))

    incli = math.sqrt(pitch**2 + roll**2) * (180 / math.pi)
    orient = ((math.atan2(roll, pitch) * (180 / math.pi)))
    if orient > 0:
        orient = 359 - orient

    if orient < 0:
        orient = abs(orient)







#    incli = ((math.acos(((cos_p * cos_r)/(math.sqrt(((sen_p*cos_r)**2) + ((sen_r)**2) + ((cos_p * cos_r)**2)))))*180)/math.pi)
#    orient = ((math.acos((sen_p * cos_r)/(math.sqrt(((sen_p * cos_r)**2) + ((sen_r)**2))))*180) / math.pi)



    print("Inclination: ", round(incli, 1), " Orientation: " ,round(orient, 1))
#    print("Encoder 1:  ", motors.motorsArray[1].getPosition(), "Encoder 2:  ", motors.motorsArray[1].getPosition(), "Encoder 3:  ", motors.motorsArray[1].getPosition())
