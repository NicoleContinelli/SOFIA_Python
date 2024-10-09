from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
import math
import numpy as np
import pandas as pd
import time

# Setting the motor's position to 0

# Motors
motors = SystemMotors(1)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([32], "SoftArmMotorConfig.json")  # motor's ids
motors.startMotors()  # start motors

print(time.sleep(3)) # response time
motors.setupPositionsMode(3,3)  # setting velocity and acceleration values
print(time.sleep(3))

#motors.setPositions([2])

'''for i in np.arange(0, 20, 0.5): 
    time.sleep(2)
    print(motors.setPositions([i]))
    #print(motors.motorsArray[0].getPosition())
#motors.setPositions([-2])'''

