import math
import numpy as np
import pandas as pd


from SystemMotors import SystemMotors
from InverseKinematics import InverseKinematics
from Sensor import Sensor

# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1, 2, 3])  # motor's ids
motors.startMotors()  # start motors

for i in range(0, 1000):
    print([amp for amp in motors.getFilterdAmps()])
