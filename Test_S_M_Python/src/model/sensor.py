# Sensor class, for managing the IMU sensor

import SerialComm as sc
import attitude_estimator as ae
import imu3dmgx510 as imu
import math
import numpy as np


class Sensor:
    def __init__(self):
        self.freq = 50
        self.my_sensor = imu.IMU3DMGX510("/dev/ttyUSB0", self.freq)
        self.pitch = np.double()
        self.roll = np.double()
        self.yaw = np.double()

    # This function enables the stream
    def sensorStream(self):
        self.my_sensor.set_streamon()

    # Get the pitch, roll and yaw of the neck, by the sensor
    def getPitch(self):
        pitch = self.my_sensor.GetPitch(self.pitch, self.roll, self.yaw)
        return pitch

    def getRoll(self):
        roll = self.my_sensor.GetRoll(self.pitch, self.roll, self.yaw)
        return roll

    def getYaw(self):
        yaw = self.my_sensor.GetRoll(self.pitch, self.roll, self.yaw)
        return yaw


