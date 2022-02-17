import math
import numpy as np
import pandas as pd

class DataCollection:

    def __init__(self):
        self.pitch = np.double()
        self.roll = np.double()
        self.yaw = np.double()

        self.cos_p = np.double()
        self.cos_r = np.double()
        self.sen_p = np.double()
        self.sen_r = np.double()

        self.incli = np.double()
        self.orient = np.double()


    # Returning inclination and orientation of the neck in Degrees 
    def data_neck_sensor(self, mi_sensor):

        self.pitch = mi_sensor.getPitch()
        self.roll = mi_sensor.getRoll()
        self.yaw = mi_sensor.getYaw()

        self.cos_p = math.cos(self.pitch)
        self.cos_r = math.cos(self.roll)
        self.sen_p = math.sin(self.pitch)
        self.sen_r = math.sin(self.roll)

        self.incli = math.sqrt(self.pitch**2 + self.roll**2) * (180 / math.pi)
        self.orient = ((math.atan2(self.roll, self.pitch) * (180 / math.pi)))

        # Conditions for having 360 degrees in orientation
        if self.orient > 0:
            self.orient = 359 - self.orient

        if self.orient < 0:
            self.orient = abs(self.orient)

        
        return self.incli, self.orient

    # Returning the encoders value
    def data_neck_motors(self, motors):
        return motors.motorsArray[0].getPosition(), motors.motorsArray[1].getPosition(), motors.motorsArray[2].getPosition()
