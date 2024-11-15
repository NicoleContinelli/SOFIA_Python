import joblib
import sklearn.utils
from sklearn.model_selection import train_test_split
import tensorflow as tf
import numpy as np
import pandas as pd
import math
# import seaborn as sns
from sklearn.utils import shuffle
from sklearn import preprocessing


# dataset read
data = pd.read_csv(
    '/home/sofia/SOFIA_Python/data/Data_2022/data_november/data_orient10.csv',)

data = sklearn.utils.shuffle(data)  # aleatorizamos los datos

# separate data in train and test
X = data.iloc[:, :2]
y = data.iloc[:, 2:]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# neural network
neuronas = 25
h_layer_1 = tf.keras.layers.Dense(units=neuronas, input_shape=[
                                  2], activation=tf.nn.tanh)
h_layer_2 = tf.keras.layers.Dense(units=neuronas, activation=tf.nn.tanh)
h_layer_3 = tf.keras.layers.Dense(units=neuronas, activation=tf.nn.tanh)
h_layer_4 = tf.keras.layers.Dense(units=neuronas, activation=tf.nn.tanh)
h_layer_5 = tf.keras.layers.Dense(units=neuronas, activation=tf.nn.tanh)
h_layer_6 = tf.keras.layers.Dense(units=neuronas, activation=tf.nn.tanh)
h_layer_7 = tf.keras.layers.Dense(units=neuronas, activation=tf.nn.tanh)
h_layer_8 = tf.keras.layers.Dense(units=neuronas, activation=tf.nn.tanh)
h_layer_9 = tf.keras.layers.Dense(units=neuronas, activation=tf.nn.tanh)
h_layer_10 = tf.keras.layers.Dense(units=neuronas, activation=tf.nn.tanh)
output = tf.keras.layers.Dense(units=3, activation=tf.nn.elu)
model_2 = tf.keras.Sequential([h_layer_1, h_layer_2, h_layer_3, h_layer_4, h_layer_5, h_layer_6, h_layer_7, h_layer_8, h_layer_9, h_layer_10,
                               output])

model_2.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss='mean_squared_logarithmic_error',
    metrics=['accuracy'],
    jit_compile=True
)

print("Initializing training ...")
# steps_per_epoch=math.ceil(), verbose=False
trained_model_2 = model_2.fit(X_train, y_train, epochs=5)
print("Succesfully trained")

# Test model using testing dataset
test_loss, test_accuracy = model_2.evaluate(X_test, y_test)
print('Test Dataset accuracy:', format(round(float(test_accuracy), 2)))

pred = []
for inclination in range(5, 36, 5):
    for orientation in range(1, 361, 10):
        # print("Let's make a prediction in orietation")
        prediction = model_2.predict(
            [[inclination, orientation]], verbose=False)
        prediction_1 = prediction.flatten().tolist()
        pred.append(prediction_1)

columns = ['Pred-M1', 'Pred-M2', 'Pred-M3']
dataset_pred = pd.DataFrame(pred, columns=columns)
print(dataset_pred)

# Saving the model
joblib.dump(model_2, '/home/sofia/SOFIA_Python/ml/trained_model2_v3.pkl')
