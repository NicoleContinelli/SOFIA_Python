import numpy as np
import pandas as pd
import math

col_incli = ['I']
col_orient = ['O']
incli = []
orient = []

for i in range(5, 26, 5):
    for o in range(5, 361, 10):
        for repeat in range(100):
            incli.append(i)
            orient.append(o)

# Convert the inclination and orientation to a df
df_incli = pd.DataFrame(incli, columns=col_incli)
df_orient = pd.DataFrame(orient, columns=col_orient)

# Load the data with the predicted values
data_IK = pd.read_csv(
    '/home/sofia/SOFIA_Python/data/Data_2022/data_november/data_orient10_v2.csv')

data_IK = data_IK.iloc[:, :2]

data_error = pd.concat([df_incli, df_orient, data_IK], axis=1,)

error_i = data_error['I'] - data_error['Inclination']
error_o = data_error['O'] - data_error['Orientation']
data_error.insert(4, "Error_I", error_i)
data_error.insert(5, "Error_O", error_o)

data_error.to_csv(
    '/home/sofia/SOFIA_Python/data/Data_2022/data_november/data_error_orient10_v2.csv', index=False)
