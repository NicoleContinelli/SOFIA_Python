# InverseKinematics class, for managing the wire lengths and the motor's movements

import math
import numpy as np


class InverseKinematics:

    # incli and orient (in degrees)
    def __init__(self, incli, orient):
        self.incli = incli * math.pi/180
        self.orient = orient * math.pi/180

    # Inverse kinematics
    def neckInverseKinematics(self):
        # Kinematics parameters
        a = 0.045  # m distance between A and base
        b = 0.045  # m distance between B and mobile platform
        L0 = 0.116+0.09  # Neck Lenght
        radious = 0.0065  # Radious of the motor
        theta = self.incli

        if (self.incli == 0):
            theta = 0.001 * math.pi/180
        phi = self.orient

        t11 = math.pow(math.sin(phi), 2) + math.cos(theta) * \
            math.pow(math.cos(phi), 2)
        t12 = (math.cos(theta)-1) * math.cos(phi) * math.sin(phi)
        t21 = t12
        t13 = math.sin(theta) * math.cos(phi)
        t31 = -t13
        t23 = math.sin(theta) * math.sin(phi)
        t32 = -t23
        t22 = math.pow(math.cos(phi), 2) + math.cos(theta) * \
            math.pow(math.sin(phi), 2)
        t33 = math.cos(theta)

        # new position of the sensor
        matrix_A = np.matrix([[-a,                 0.5*a,              0.5*a],
                             [0, (-(math.sqrt(3)*a/2)), (math.sqrt(3)*a/2)],
                             [0,                     0,                  0],
                             [1,                     1,                  1]])

        matrix_B = np.matrix([[-b,                 0.5*b,              0.5*b],
                             [0, (-(math.sqrt(3)*b/2)), (math.sqrt(3)*b/2)],
                             [0,                     0,                  0],
                             [1,                     1,                  1]])
        '''
        matrix_A = np.matrix([[0, (-math.sqrt(3)*a/2), (math.sqrt(3)*a/2)],
                             [ a,               -0.5*a,            -0.5*a],
                             [ 0,                    0,                 0],
                             [ 1,                    1,                 1]])
        matrix_B = np.matrix([[0, (-math.sqrt(3)*b/2), (math.sqrt(3)*b/2)],
                             [ b,              -0.5*b,             -0.5*b],
                             [ 0,                   0,                  0],
                             [ 1,                   1,                 1]])
        '''
        # Rotational Matrix
        matrix_R = np.matrix([[t11, t12, t13],
                             [t21, t22, t23],
                             [t31, t32, t33]])

        # s0 and t0
        s0 = L0 * (1 - math.cos(theta)) / theta
        t0 = L0 * math.sin(theta) / theta

        # Translation Matrix
        matrix_P = np.matrix([[s0 * math.cos(phi)],
                             [s0 * math.sin(phi)],
                             [t0]])

        matrix_T = np.matrix([[matrix_R[0, 0], matrix_R[0, 1], matrix_R[0, 2], matrix_P[0, 0]],
                             [matrix_R[1, 0], matrix_R[1, 1],
                                 matrix_R[1, 2], matrix_P[1, 0]],
                             [matrix_R[2, 0], matrix_R[2, 1],
                                 matrix_R[2, 2], matrix_P[2, 0]],
                             [0, 0, 0, 1]])

        # Lengths Matrix
        matrix_L = np.dot(matrix_T, matrix_B) - matrix_A

        # Wire final lengths
        L1 = math.sqrt((matrix_L[0, 0]**2) +
                       (matrix_L[1, 0]**2) + (matrix_L[2, 0]**2))
        L2 = math.sqrt((matrix_L[0, 1]**2) +
                       (matrix_L[1, 1]**2) + (matrix_L[2, 1]**2))
        L3 = math.sqrt((matrix_L[0, 2]**2) +
                       (matrix_L[1, 2]**2) + (matrix_L[2, 2]**2))

        # Angles variations (radians)
        theta_1 = (L0 - L1) / radious
        theta_2 = (L0 - L2) / radious
        theta_3 = (L0 - L3) / radious

        return theta_1, theta_2, theta_3
    


    # Inverse kinematics
    def armInverseKinematics(self):
        a=0.035 #m distance between A and base
        b=0.035 #m distance between B and mobile platform
        L0=0.2 #Arm Lenght

        '''if (self.incli == 0):
            theta = 0.001 * math.pi/180
        phi = self.orient'''


    #Pendiente
    #Calcular angulo de bloque y usar arco

        #R=L0/theta
        radious = L0/self.incli

        L1 = self.incli/1.5

        L2 = (self.orient/1.732) - (self.incli/3)

        L3 = (-self.orient/1.732) - (self.incli/3)

        # Angles variations (radians)
        theta_1 = (L0 - L1) / radious
        theta_2 = (L0 - L2) / radious
        theta_3 = (L0 - L3) / radious

        return theta_1, theta_2, theta_3