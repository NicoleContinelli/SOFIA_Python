# DirectKinematics class, for managing the wire lengths and the motor's movements

import math
import numpy as np


class DirectKinematics:

    # incli and orient (in degrees)
    def __init__(self, theta1, theta2, theta3):
        self.theta1 = theta1
        self.theta2 = theta2
        self.theta3 = theta3

    # Inverse kinematics
    def neckDirectKinematics(self):
        # Kinematics parameters
        a = 0.045  # m distance between A and base
        b = 0.045  # m distance between B and mobile platform
        L0 = 0.116 + 0.09  # Neck Lenght
        radious = 0.0065  # Radious of the motor

        # lengths
        L1 = L0 - (self.theta1 * radious)
        L2 = L0 - (self.theta2 * radious)
        L3 = L0 - (self.theta3 * radious)

        orient = abs(np.degrees(
            math.atan(((L3+L2)-(2*L1))/(math.sqrt(3)*(L2-L3)))))
        incli = abs(np.degrees(
            2 * math.asin(((L2-L3)/(2*math.sqrt(3)*a*math.cos(np.radians(orient)))))))

        return incli, orient
