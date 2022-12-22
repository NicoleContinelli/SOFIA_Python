# Motor class, for managing the motor's encoder (SINGLE motor)

import SocketCanPort as scp
import CiA402SetupData as CiA402sd
import Cia402device as Cia402d
import json as js
import os
import numpy as np


class Motor:

    # Json file that allows to load the characteristics of the motor (Neck Json file)
    def __init__(self, idMotor, nameFile):
        with open(os.path.dirname(os.path.realpath(__file__)) + "/" + nameFile) as neckFile:
            config = js.load(neckFile)
        self.pm = scp.SocketCanPort(config["canPort"])
        self.sd = CiA402sd.CiA402SetupData(config["new_encRes"], config["new_mlRatio"], config["new_SampSL"],
                                           config["motor_current_limit"], config["drive_current_limit"])
        # create an instance of Cia402d
        self.motor = Cia402d.CiA402Device(idMotor, self.pm, self.sd)

    # These methods are actions that a SINGLE motor can execute
    def startMotor(self):
        self.motor.Reset()
        # Internally we are calling a function of "Cia402d" library, by the motor instance in the constructor
        self.motor.SwitchOn()

    def stopMotor(self):
        self.motor.SwitchOff()

    def setupPositionMode(self, vel, accel):
        self.motor.SetupPositionMode(vel, accel)

    def setPosition(self, theta):
        self.motor.SetPosition(theta)

    def getPosition(self):
        return self.motor.GetPosition()

    def getAmp(self):
        return self.motor.GetAmps()

    def getFilteredAmps(self, n_samples):
        data = np.array([])
        for i in range(n_samples):
            np.append(data, self.motor.GetAmps())
        print(data)
        return np.mean(data)

    def getVelocity(self):
        return self.motor.GetVelocity()
