# SOFIA_Python
This repository includes the traduction of C++ to Python library (Driver motors and IMU Sensor)

## 1. Introduction
The HUMASOFT project at the time, developed C++ libraries for the movement of Cia402 type engine drivers via CAN communication and a library for the management of IMU type sensors in soft robotics. REPO: https://github.com/HUMASoft. Now HUMASOFT becomes the SOFIA project, which takes a specific target on how to apply machine learning to soft robotic articulations. That's why these C++ libraries were translated to Python. 

## 2. Stuffs to consider
- Since these libraries use CAN communication, they need the "can-utils" package. This can only be installed by Linux OS by terminal.
```bash
sudo apt-get install can-utils
```
- Make sure you have a Python version higher than 3.4 installed.
- 



