


from Sensor import Sensor
import math
import numpy as np

# Knowing the Inclination and Orientation of the sensor, with a prevoius motor position
mi_sensor = Sensor()
mi_sensor.sensorStream()

for i in np.arange(0, 20, 0.02):
    pitch = mi_sensor.getPitch()
    roll = mi_sensor.getRoll()
    yaw = mi_sensor.getYaw()

    cos_p = math.cos(pitch)
    cos_r = math.cos(roll)
    sen_p = math.sin(pitch)
    sen_r = math.sin(roll)

    print("Pitch:  ", round(pitch * (180 / math.pi), 2), "Roll:  ", round(roll * (180 / math.pi), 2))

#    incli = math.sqrt(pitch**2 + roll**2) * (180 / math.pi)
#    orient = ((math.atan2(roll, pitch) * (180 / math.pi)))
    incli = ((math.acos(((cos_p * cos_r)/(math.sqrt(((sen_p*cos_r)**2) + ((sen_r)**2) + ((cos_p * cos_r)**2)))))*180)/math.pi)
    orient = ((math.acos((sen_p * cos_r)/(math.sqrt(((sen_p * cos_r)**2) + ((sen_r)**2))))*180) / math.pi) - 90



#    print("Inclination: " + str(round(incli, 1)) + " Orientation: " + str(round(orient, 1)))
