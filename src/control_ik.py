from model.sensor import Sensor
from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
import math
import numpy as np
import pandas as pd
import joblib


# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1, 2, 3])  # motor's ids
motors.startMotors()  # start motors

# Sensor
mi_sensor = Sensor()
mi_sensor.sensorStream()

incli_target = 20
orient_target = 90

# instantiate InverseKinematics class
kine1 = InverseKinematics(incli_target, orient_target)
theta1, theta2, theta3 = kine1.neckInverseKinematics()  # saving the length's cables

motors.setupPositionsMode(12, 12)
motors.setPositions([theta1, theta2, theta3])

# Kowing the sensor lecture after setting the IK position
ik_incli, ik_orient = mi_sensor.readSensor(mi_sensor)

# Model trained
model_reg = joblib.load('/home/sofia/SOFIA_Python/ml/trained_error.pkl')

# Parameters of the DataFrame
cols = ['Inclination', 'Orientation']
data = []
new_orien = 0
new_incli = 0
error = 0.03

while (error > 0.02):
    pred = model_reg .predict(
        [[incli_target, orient_target, ik_incli, ik_orient]])
    pred = pred.flatten().tolist()
    er_incli = pred[0]
    er_orien = pred[1]
    new_incli = incli_target+er_incli
    new_orien = orient_target+er_orien
    ki_control = InverseKinematics(new_incli, new_orien)
    # saving the length's cables
    theta1, theta2, theta3 = ki_control.neckInverseKinematics()
    motors.setPositions([theta1, theta2, theta3])

    for i in np.arange(0, 0.04, 0.02):
        ik_inlci, ik_orient = mi_sensor.readSensor(mi_sensor)

        # print("Inclination: ", round(ik_inlci, 1), " Orientation: ", round(ik_orient, 1))
        print("error Inclination: ", round(incli_target-ik_inlci, 1),
              " error Orientation: ", round(orient_target - ik_orient, 1))
