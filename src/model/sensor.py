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

    def readSensor(self, mi_sensor):
        pitch = mi_sensor.getPitch()
        roll = mi_sensor.getRoll()
        yaw = mi_sensor.getYaw()

        cos_p = math.cos(pitch)
        cos_r = math.cos(roll)
        sen_p = math.sin(pitch)
        sen_r = math.sin(roll)

        incli = math.sqrt(pitch**2 + roll**2) * (180 / math.pi)
        orient = ((math.atan2(roll, pitch) * (180 / math.pi)))

        # Conditions for having 360 degrees in orientation
        if orient > 0:
            orient = orient

        if orient < 0:
            orient = 360 - abs(orient)

        return incli, orient
