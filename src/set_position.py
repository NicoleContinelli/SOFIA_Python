from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
import math
import numpy as np
import pandas as pd
import time

# Setting the motor's position to 0

# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1, 2, 3], "SoftNeckMotorConfigOld.json")  # motor's ids

# motors.setupPositionsMode(12, 12)  # setting velocity and acceleration values
# motors.setPositions([12])

motors.startMotors()

time.sleep(2)

motors.setupPositionsMode(6,6)
# posicion_0 = list(motors.getPositions())

# print("Posicion actual:", posicion_0)

time.sleep(1)

motors.setPositions([0, 0, 0])

# while True:
#      print(list(motors.getPositions()))
#      time.sleep(0.2)