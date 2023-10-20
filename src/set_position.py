from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
import math
import numpy as np
import pandas as pd
import time

# Setting the motor's position to 0

# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1, 2, 3])  # motor's ids
motors.startMotors()  # start motors

motors.setupPositionsMode(12, 12)  # setting velocity and acceleration values
motors.setPositions([0,27,0])
