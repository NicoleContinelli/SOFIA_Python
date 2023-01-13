import math
import numpy as np
import pandas as pd
import joblib
import time

from model.system_motors import SystemMotors
from model.sensor import Sensor
from model.data_collection import DataCollection
from model.inverse_kinematics import InverseKinematics

# THIS IS ONLY A .PY FOR OBTAINING THE RECTIFIED THETAS, AFTER WE RECTIFIED THE INCLINATION AND ORIENTATION 
# Parameters of the DataFrame
thetas_rectified = []
cols = ['M1_R', 'M2_R', 'M3_R']
data_col = DataCollection()  # instantiate DataCollection class


# Load the data with the predicted values
data_target = pd.read_csv('/home/sofia/SOFIA_Python/data/Data_2023/data_january/data_rectified.csv')


for i in range(len(data_target)):
    # IK
    kine1 = InverseKinematics(data_target['I_rectified'][i], data_target['O_rectified'][i])
    theta1, theta2, theta3 = kine1.neckInverseKinematics()  # saving the length's cables
    thetas = [theta1, theta2, theta3]
    thetas_rectified.append(thetas)
    
# adding the data values (array type), to the data frame
df = pd.DataFrame(thetas_rectified, columns=cols)
df.to_csv(
        '/home/sofia/SOFIA_Python/data/Data_2023/data_january/data_rectified_thetas_IK.csv', index=False)
        
print("Data Ready")
