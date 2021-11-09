import SocketCanPort as scp
import CiA301CommPort
import CiA402SetupData as CiA402sd
import Cia402device as Cia402d


class startMotors:

    def __init__(self):
        self.pm1 = scp.SocketCanPort("can1")
        self.pm2 = scp.SocketCanPort("can1")
        self.pm3 = scp.SocketCanPort("can1")

        self.sd1 = CiA402sd.CiA402SetupData(2048, 24, 0.001, 0.144, 20)
        self.sd2 = CiA402sd.CiA402SetupData(2048, 24, 0.001, 0.144, 20)
        self.sd3 = CiA402sd.CiA402SetupData(2048, 24, 0.001, 0.144, 20)

        self.motor1 = Cia402d.CiA402Device(1, self.pm1, self.sd1)  # motor object
        self.motor2 = Cia402d.CiA402Device(2, self.pm2, self.sd2)
        self.motor3 = Cia402d.CiA402Device(3, self.pm3, self.sd3)

    def startMotor1(self):
        self.motor1.Reset()
        self.motor1.SwitchOn()

    def startMotor2(self):
        self.motor2.Reset()
        self.motor2.SwitchOn()

    def startMotor3(self):
        self.motor3.Reset()
        self.motor3.SwitchOn()

'''
        def __init__(self, idMotor, nameFile="softNeckMotorConfig.json"):
            with open("/home/humasoft/PythonProject/Test_S_M_Python/"+nameFile) as f:
                config = js.load(f)
            self.pm = scp.SocketCanPort(config["canPort"])
            self.sd = CiA402sd.CiA402SetupData(config["new_encRes"], config["new_mlRatio"], config["new_SampSL"],
            config["motor_current_limit"], config["drive_current_limit"])
            self.motor = Cia402d.CiA402Device(idMotor, self.pm, self.sd)
'''
