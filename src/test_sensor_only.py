import time
import csv
import numpy as np
import math
import imu3dmgx510 as imu  # tu módulo IMU

class Sensor:
    def __init__(self):
        self.freq = 1  # Frecuencia de muestreo en Hz
        self.my_sensor = imu.IMU3DMGX510("/dev/ttyUSB0", self.freq)
        self.pitch = np.double()
        self.roll = np.double()
        self.yaw = np.double()

    def sensorStream(self):
        self.my_sensor.set_streamon()

    def getPitch(self):
        return self.my_sensor.GetPitch(self.pitch, self.roll, self.yaw)

    def getRoll(self):
        return self.my_sensor.GetRoll(self.pitch, self.roll, self.yaw)

    def getYaw(self):
        return self.my_sensor.GetYaw(self.pitch, self.roll, self.yaw)


# Inicializar sensor
sensor_imu = Sensor()
sensor_imu.sensorStream()

# Guardar tiempo de inicio
start_time = time.time()

# Abrir CSV
with open("imu_data.csv", mode="w", newline="") as file:  
    writer = csv.writer(file)
    writer.writerow(["Time(s)", "Roll", "Pitch", "Yaw"])

    for i in np.arange(0, 120, 0.02):
        roll = sensor_imu.getRoll() * (180 / math.pi)
        pitch = sensor_imu.getPitch() * (180 / math.pi)
        yaw = sensor_imu.getYaw() * (180 / math.pi)

        # Tiempo relativo desde el inicio
        elapsed = time.time() - start_time

        print(f"Time: {elapsed:.2f} s | Roll: {roll:.1f} | Pitch: {pitch:.1f} | Yaw: {yaw:.1f}")

        # Guardar en CSV
        writer.writerow([round(elapsed, 2), round(roll, 2), round(pitch, 2), round(yaw, 2)])
