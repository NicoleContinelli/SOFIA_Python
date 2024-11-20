from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
import math
import numpy as np
import pandas as pd
import time

# Setting the motor's position to 0

# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors >> OJO CHANGE IT DEPENDING ON THE # OF MOTORS
motors.loadMotors([31, 32, 33], "SoftArmMotorConfig.json")  # motor's ids
motors.startMotors()  # start motors

print(time.sleep(2)) # response time
motors.setupPositionsMode(3,3)  # setting velocity and acceleration values
print(time.sleep(2))

motors.setPositions([0,-2.5,-3.9])

'''for i in np.arange(0, 20, 0.5): 
    time.sleep(2)
    print(motors.setPositions([i]))
    #print(motors.motorsArray[0].getPosition())
#motors.setPositions([-2])'''

