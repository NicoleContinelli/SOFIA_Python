from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
import math
import numpy as np

# Knowing the Inclination and Orientation of the sensor, with a prevoius motor position

# Motorsml
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1, 2, 3], "SoftNeckMotorConfig.json")  # motor's ids
#motors.loadMotors([31, 32, 33], "SoftArmMotorConfig.json")  
motors.startMotors()  # start motors

pos = [0, 0, 0]  # initial position
diff = [1, 1, 1]  # difference
baseCurrent = 40

for i in range(10000):
    vels = [val for val in motors.getVelocity()]
    if vels < [1, 1, 1] and vels > [-1, -1, -1]:
        amps = motors.getAmps()
        diff = [(baseCurrent - amp)/10000 for amp in amps]
        pos = [pos[i] + diff[i] for i in range(len(pos))]
        motors.setupPositionsMode(10, 10)
        motors.setPositions(pos)

pos = [val for val in motors.getPositions()]
print(pos)
