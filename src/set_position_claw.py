from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
import math
import numpy as np
import pandas as pd
import time

# Setting the motor's position to 0

# Motors
motors = SystemMotors(2)  # instantiate SystemMotors class >> number of motors >> OJO CHANGE IT DEPENDING ON THE # OF MOTORS
motors.loadMotors([1,2], "SoftClawMotorConfig.json")  # motor's ids
motors.startMotors()  # start motors

print(time.sleep(2)) # response time
motors.setupPositionsMode(1,1)  # setting velocity and acceleration values

#kine1 = InverseKinematics(25, 90)
#theta1, theta2 = kine1.clawInverseKinematics()  # saving the length's cables
#print('PRINTING THETAS...', theta1, theta2)
#motors.setPositions([3*math.pi/4])
motors.setPositions([3*math.pi/4, -3*math.pi/4])
print("Posicion 3 pi cuartos")
#print(motors.motorsArray[0].getPosition(), motors.motorsArray[1].getPosition())
print(time.sleep(7))
print("Posicion a 0")
motors.setPositions([0, 0])

'''for i in np.arange(0, 20, 0.5): 
    time.sleep(2)
    print(motors.setPositions([i]))
    #print(motors.motorsArray[0].getPosition())
#motors.setPositions([-2])'''

