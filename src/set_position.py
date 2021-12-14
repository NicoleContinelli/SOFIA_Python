from model.sensor import Sensor
from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
import math
import numpy as np
import pandas as pd

# Setting the motor's position to 0

# Motors
motors = SystemMotors(1)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([3])  # motor's ids
motors.startMotors()  # start motors

motors.setupPositionsMode(12, 12) #setting velocity and acceleration values
motors.setPositions([9.42]) 

'''
if motors.motorsArray[0].getPosition() != 0:
    motors.motorsArray[0].getPosition() = 0
    
print(motors.motorsArray[0].getPosition(), motors.motorsArray[1].getPosition(), motors.motorsArray[2].getPosition())
'''
