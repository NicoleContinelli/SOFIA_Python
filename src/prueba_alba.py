#Librerias
from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
import math
import numpy as np
import pandas as pd
import time
from model.sensor import Sensor
import csv

import math
import numpy as np
import pandas as pd
import joblib

import matplotlib.pyplot as plt
from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
from model.sensor import Sensor

#xx = [i/1 for i in range(175)]
def plot_two_function(title, y1_1, y1_2, y2_1, y2_2, t, color1, color2, label1, label2, label3):
    plt.figure(figsize=(15,15))
    
    plt.subplot(2, 1, 1)
    plt.grid()
    plt.plot(t, y1_1, color = color1, label = label1, linestyle = 'dashdot', linewidth = 3.5)
    plt.plot(t, y1_2, color = color2, label = label2, linewidth = 1.5)
    plt.ylabel("Inclinación (grados)")
    plt.title(title)
    plt.legend()
    
    plt.subplot(2, 1, 2)
    plt.grid()
    plt.xlabel("Tiempo (segundos)")
    plt.ylabel("Orientación (grados)")
    plt.plot(t, y2_1, color = color1, label = label1, linestyle = 'dashdot', linewidth = 3.5)
    plt.plot(t, y2_2, color = color2, label = label3, linewidth = 1.5)
    plt.legend()
    plt.savefig('MLP_v7_pruebahoy.png')
    return plt.show()




"""
# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1, 2, 3])  # motor's ids
motors.startMotors()  # start motors

# Sensor
mi_sensor = Sensor()  # instantiate Sensor class
mi_sensor.sensorStream()  # enable sensor

# Initial positions
orientation = 0
inclination = 0

# Parameters of the DataFrame
cols = ['Inclination', 'Orientation', 'M1', 'M2', 'M3']
data = []
motors.setupPositionsMode(12, 12)  # setting velocity and acceleration values

# ML
model_reg = joblib.load('data/Data_prueba_alba/model_prueba.pkl')


# Inclination's repetition
for inclination in range(5, 36, 5):

    # Orientation's repetition
    for orientation in range(1, 361, 10):

        pred = model_reg.predict([[inclination, orientation]])
        thetas = pred.flatten().tolist()
        motors.setPositions([thetas[0], thetas[1], thetas[2]])

        # Knowing the Inclination and Orientation of the sensor, with a previous motor position
        for i in np.arange(0, 2, 0.02):  # time sampling >> steps of 0.02
            incli, orient = mi_sensor.readSensor(mi_sensor)

            print("Inclination: ", round(incli, 1),
                  " Orientation: ", round(orient, 1))

            # Adding the values of incli, orient and encoders in "data"
            data.append([incli, orient, motors.motorsArray[0].getPosition(
            ), motors.motorsArray[1].getPosition(), motors.motorsArray[2].getPosition()])

    # adding the data values (array type), to the data frame
    df = pd.DataFrame(data, columns=cols)
    # print(df)
    df.to_csv(
        'data/Data_prueba_alba/data_model_Predictions1.csv', index=False)
    df.info()

    print("Inclination: ", round(incli, 1), " Orientation: ", round(orient, 1))

print("Data Ready")
"""


from model.sensor import Sensor
from model.system_motors import SystemMotors
from model.inverse_kinematics import InverseKinematics
import math
import numpy as np
import pandas as pd
import keras

# Knowing the Inclination and Orientation of the sensor, with a prevoius motor position

# Motors
motors = SystemMotors(3)  # instantiate SystemMotors class >> number of motors
motors.loadMotors([1, 2, 3])  # motor's ids
motors.startMotors()  # start motors

# Sensor
mi_sensor = Sensor()
mi_sensor.sensorStream()

# ML
model_reg = joblib.load('/home/sofia/SOFIA_Python/ml/Notebooks/prueba_model4.pkl')

"""
kine1 = InverseKinematics(25, 180)  # instantiate InverseKinematics class
theta1, theta2, theta3 = kine1.neckInverseKinematics()  # saving the length's cables
motors.setPositions([theta1, theta2, theta3])

"""


incli_target = 34
orient_target = 307

pred = model_reg.predict([[incli_target, orient_target]])
thetas = pred.flatten().tolist()

motors.setupPositionsMode(12, 12)
motors.setPositions([thetas[0], thetas[1], thetas[2]])


for i in np.arange(0, 15, 0.02):
    inclination, orientation = mi_sensor.readSensor(
        mi_sensor)  # new method of teh sensor class

    print("Inclination: ", round(inclination, 1),
          " Orientation: ", round(orientation, 1))

plot_two_function("Control de lazo cerrado de la Cinemática Inversa - MLP datos ajustados a la recta",
                 incli_target,inclination,orient_target,orientation, 750,
                 "black", "#FFC30F", 
                 "Referencia","Inclinación - CI","Orientación - CI")

motors.setPositions([0,0,0])