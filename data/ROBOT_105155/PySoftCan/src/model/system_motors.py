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
    def loadMotors(self, index, articulationFile):
        assert self.numMotors == len(index)

        for i in index:
            # calling the "Motor" class
            self.motorsArray.append(Motor(i, articulationFile)) # Here you put the .json config file

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
        return [motor.getAmp() for motor in self.motorsArray]

    def getFilteredAmps(self, n_samples):
        return [motor.getFilteredAmps(n_samples) for motor in self.motorsArray]

    def Setup_Velocity_Mode(self, vel):
        for motor in self.motorsArray:
            motor.Setup_Velocity_Mode(vel)

    def getVelocity(self):
        for motor in self.motorsArray:
            yield motor.getVelocity()

    def Setup_Torque_Mode(self):
        for motor in self.motorsArray:
            motor.Setup_Torque_Mode()
    
    def setTorque(self, torqArray):
        assert self.numMotors == len(torqArray)

        for i, torq in enumerate(torqArray):
            self.motorsArray[i].setTorque(torq)