import math
import numpy as np
import pandas as pd
import joblib
import time

from model.system_motors import SystemMotors
from model.sensor import Sensor
from model.data_collection import DataCollection
from model.inverse_kinematics import InverseKinematics

'''
THIS IS ONLY A .PY FOR OBTAINING THE RECTIFIED THETAS, AFTER WE RECTIFIED THE INCLINATION AND ORIENTATION 

Explanation:
1. We create a function "inputs" to generate a dataframe, that have I and O rectified. This data is taken from the data extraction
of the robotic neck. (We calculated the following: I and O theoric, I and O error, and I and O rectified)

2. Then we create a function called "outputs" that consists in a list called "thetas_rectified" and here we save the thetas of the inverse kinematics. To the object "InverseKinematics" 
I and O rectified target values are passed as arguments. 

3. After that we extract the rectified thetas, and save them in the "thetas_rectified" array.

4. Then we created a function called "training data" to concat inputs and outputs in a dataframe with those reftified thetas, I an O theorics and their errors
'''



#-------------------------------------------------------------------------------------------------------------------------- 
# Create a table with the error and the rectified Angles
def inputs(df_10):
  df = pd.DataFrame() ## Hacemos un dataframe para meter los valores de inclinacion y orientacion teoricos
  incli = []
  orient = []

  for i in range(5,36,5):
    for o in range(5,361,10):
      for repeat in range(100):
        incli.append(i)
        orient.append(o)

  #Convert the inclination and orientation to a df
  df['I'] = incli
  df['O'] = orient

  # Añadimos columnas a df renombradas 
  df['Inclination_sensor'] = df_10['Inclination']
  df['Orientation_sensor'] = df_10['Orientation'] 

  df['M1_IK']= df_10['M1'] 
  df['M2_IK']= df_10['M2'] 
  df['M3_IK']= df_10['M3'] 

  # Añadir errorres
  df['I_error'] = df['I'] - df['Inclination_sensor']
  df['O_error'] = df['O'] - df['Orientation_sensor']

  df['I_rectified'] = df['I'] + df['I_error']
  df['O_rectified'] = df['O'] + df['O_error']

  return df


# THETAS RECTIFIED
# Parameters of the DataFrame
def outputs(data_target):
    thetas_rectified = []
    cols = ['M1_R', 'M2_R', 'M3_R']


    for i in range(len(data_target)):
        # IK
        kine1 = InverseKinematics(data_target['I_rectified'][i], data_target['O_rectified'][i])
        theta1, theta2, theta3 = kine1.neckInverseKinematics()  # saving the length's cables
        thetas = [theta1, theta2, theta3]
        thetas_rectified.append(thetas)
        
    # adding the data values (array type), to the data frame
    df_thetas_rectified = pd.DataFrame(thetas_rectified, columns=cols)

    data_error_theta = pd.concat([data_target[['M1_IK','M2_IK','M3_IK']], df_thetas_rectified], axis=1)
    data_error_theta['M1_error'] = data_error_theta['M1_IK'] - data_error_theta['M1_R']
    data_error_theta['M2_error'] = data_error_theta['M2_IK'] - data_error_theta['M2_R']
    data_error_theta['M3_error'] = data_error_theta['M3_IK'] - data_error_theta['M3_R']

    return data_error_theta


def data_training(df_input, df_output):
    data_model = pd.DataFrame()
    data_model = pd.concat([df_input[['I','O','I_error','O_error']], df_output[['M1_error','M2_error', 'M3_error']]], axis=1)

    return data_model


#-------------------------------------------------------------------------------------------------------------------------- 




# Load the data and preprocessed it to extract the I and O rectified
df1_10 = pd.read_csv('/home/sofia/SOFIA_Python/data/Data_2023/data_february/data_orient10_MASTER_24.csv')
data_target = inputs(df1_10)

# Load the data and preprocessed it to extract the I and O rectified
data_labels = outputs(data_target)


# Final training data
df_training = data_training(data_target, data_labels)

df_training.to_csv(
        '/home/sofia/SOFIA_Python/data/Data_2023/data_february/data_training_orient10_MASTER_24.csv', index=False)
        
print("Data Ready")
