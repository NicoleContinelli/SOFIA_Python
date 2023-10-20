from model.system_motors import SystemMotors
from model.sensor import Sensor
import fcontrol as fctl
import time
import math
'''
PENDING FOR REVISIT AND COMMENTS !!!
'''
LG0 = 0.003  # meters
TRADIO = 0.0075  # radio del tambor
PRADIO = 0.05  # radio de la plataforma

motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1, 2, 3])  # motor's ids
motors.startMotors()  # start motors

# Sensor
mi_sensor = Sensor()  # instantiate Sensor class
mi_sensor.sensorStream()  # enable sensor

pitch = 1
roll = 1
yaw = 0  # Initialize yaw variable if necessary

class SamplingTime:
    def __init__(self):
        self.last_time = time.time()

    def SetSamplingTime(self, dt):
        current_time = time.time()
        elapsed_time = current_time - self.last_time
        if elapsed_time < dt:
            time.sleep(dt - elapsed_time)
        self.last_time = current_time



def tensethread(motor):
    motor.Setup_Torque_Mode()
    motor.SetTorque(0.01)  # 0.07
    time.sleep(0.3)
    while motor.GetVelocity() > 0.2:  # 0.2
        print(f"Tensing thread... vel: {motor.GetVelocity()}")
    motor.Setup_Velocity_Mode(0)
    return True

#-------------------------------------------------------------------------
# Calibrado de los hilos y control en posicion 0 de pitch y roll
# haciendo uso de controladores en velocidad externos de cada uno de los drivers */

# pitch, roll to velocity in rad/s
def pr2tendons(pitch, roll, vel):
    T = PRADIO / TRADIO
    vel[0] = pitch * T
    vel[1] = roll * T * math.sin(2 * math.pi / 3) + pitch * T * math.cos(2 * math.pi / 3)
    vel[2] = roll * T * math.sin(4 * math.pi / 3) + pitch * T * math.cos(4 * math.pi / 3)

    print("HELLOOOOOO1")

# inputs
targetPose = [0, 0]  # HOME
targetVel = [0, 0, 0]

# control loop sampling time
freq = 50  # sensor use values: 50, 100, 500...
dts = 1 / freq
Ts = SamplingTime()
print("HELLOOOOOO")
Ts.SetSamplingTime(dts)  # 0.020
print("PETOOOOOOOO")

tensed = False

tensed = tensethread(motors) and tensed
cntrl1 = fctl.PIDBlock(0.015, 36, 0, dts)
cntrl2 = fctl.PIDBlock(0.015, 36, 0, dts)
cntrl3 = fctl.PIDBlock(0.015, 36, 0, dts)



fcPitchVelocity = fctl.FPDBlock(2.5773, 3.2325, -0.8500, dts)
fcRollVelocity = fctl.FPDBlock(2.6299, 3.2395, -0.8600, dts)

fcPitchVelocity=fctl.FPDBlock.FPDBlock.OutputUpdate

for i in range(100):
    mi_sensor.GetPitchRollYaw(pitch, roll, yaw)

while (abs(pitch) > 0.005 or abs(roll) > 0.005):
    incli, orient = mi_sensor.readSensor(mi_sensor)
    
    print("Inclination: ", round(incli, 1),
        " Orientation: ", round(orient, 1))
    
    #cambio signo para igualar sentido de giro de los motores y del sensor
    pitch = -pitch
    roll  = -roll

    pitchError = targetPose[0] - pitch
    rollError = targetPose[1] - roll

    #fdfsd=fcPitchVelocity.

    pitchCs = fcPitchVelocity.OutputUpdate(pitchError)
    if not math.isfinite(pitchCs):
        pitchCs = 0.0

    rollCs = fcRollVelocity.OutputUpdate(rollError)
    if not math.isfinite(rollCs):
        rollCs = 0.0