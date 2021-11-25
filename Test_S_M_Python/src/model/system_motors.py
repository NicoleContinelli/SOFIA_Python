# SystemMotors class, for managing the all motor's encoder at the SAME time
from model.motor import Motor


class SystemMotors:
    '''
    numMotors : (integer) Number of motors that form the system
    motorsArray : (array of type Motors) Array of the motors (IDs) that compound the motor's system
    '''

    def __init__(self, numMotors):
        self.numMotors = numMotors
        self.motorsArray = []

    # Assign the motors ID
    def loadMotors(self, index):
        assert self.numMotors == len(index)

        for i in index:
            self.motorsArray.append(Motor(i, "SoftNeckMotorConfig.json")) # calling the "Motor" class

    # These methods are the same as in the "Motor" class, but know the actions are executed for ALL the motors at a time
    def startMotors(self):
        for motor in self.motorsArray:
            motor.startMotor()

    def stopMotors(self):
        for motor in self.motorsArray:
            motor.stopMotor()

    def setupPositionsMode(self, vel, accel):
        for motor in self.motorsArray:
            motor.setupPositionMode(vel, accel)

    def setPositions(self, thetaArray):
        assert self.numMotors == len(thetaArray)

        for i, theta in enumerate(thetaArray):
            self.motorsArray[i].setPosition(theta)

    def getPositions(self):
        for motor in self.motorsArray:
            yield motor.getPosition()

    def getAmps(self):
        for motor in self.motorsArray:
            yield motor.getAmp()

    def getVelocities(self):
        for motor in self.motorsArray:
            yield motor.getVelocity()
