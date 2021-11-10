# Motor class, for managing the motor's encoder (SINGLE motor)

import SocketCanPort as scp
import CiA402SetupData as CiA402sd
import Cia402device as Cia402d
import json as js
import os


class Motor:

    # Json file that allows to load the characteristics of the motor (Neck Json file)
    def __init__(self, idMotor, nameFile):
        with open(os.path.dirname(os.path.realpath(__file__)) + "/" + nameFile) as neckFile:
            config = js.load(neckFile)
        self.pm = scp.SocketCanPort(config["canPort"])
        self.sd = CiA402sd.CiA402SetupData(config["new_encRes"], config["new_mlRatio"], config["new_SampSL"],
        config["motor_current_limit"], config["drive_current_limit"])
        self.motor = Cia402d.CiA402Device(idMotor, self.pm, self.sd) # create an instance of Cia402d

    # These methods are actions that a SINGLE motor can execute
    def startMotor(self):
        self.motor.Reset()
        self.motor.SwitchOn() # Internally we are calling a function of "Cia402d" library, by the motor instance in the constructor

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

    def getVelocity(self):
        return self.motor.GetVelocity()
