# SOFIA_Python
<p align="center">
    This repository includes the traduction of C++ to Python library (Driver motors and IMU Sensor)
</p>


## 1. Introduction
<p align="justify">
The HUMASOFT project at the time, developed C++ libraries for the movement of Cia402 type engine drivers via CAN communication and a library for the management of IMU type sensors in soft robotics. REPO: https://github.com/HUMASoft. Now HUMASOFT becomes the SOFIA project, which takes a specific target on how to apply machine learning to soft robotic articulations. That's why these C++ libraries were translated to Python using SWIG. 
</p>

## 2. Stuffs to consider
<p align="justify">
<li> Since these libraries use CAN communication, they need the **can-utils** package. This can only be installed in Linux OS by terminal. </li>

```bash
sudo apt-get install can-utils
```
</p>

<p align="justify">
<li> It's recommended to update the Linux OS (i.e. if you are in Ubuntu, have at least the 18.04 LTS version). </li>
</p>

<p align="justify">
<li> If you install the Python modules in a specific i.e Ubuntu version, and you want to test them in a different one, maybe the modules are not gonna work. </li>
</p>

<p align="justify">
<li> Make sure you have a Python version higher than 3.4 installed. Also be sure that this version is the one you are going to use throughout the installation of the libraries, because at the moment you install them, they generate modules that will be saved with the Python version that is by default on your computer (the installation is in point #3). If you have several versions, use only **ONE** in all this installation process and make sure that on your terminal when you type "python3" is the newest Python version you installed, otherwise, the Python modules may not work. </li></p>

```bash
# verify your Python version 
python3 --version

# execute Python in terminal
python3
```
<p align="justify">
<li> If your newest Python version isn't the version when you type on your terminal "python3", you can follow this tutorial: https://www.youtube.com/watch?v=hAdympqE9v0 </li>
</p>

<p align="justify">
<li> It's important to emphasize that we did this for you to not worry were the libraries are. For instance, you don't need to create Python files in the same library folder, to use them. They are already located in Python globally. It's like using Numpy o Pandas after its installation. </li>
</p>

- Lastly, you will need to configure the environment variable LD_LIBRARY_PATH:

```bash
# edit the bashrc file 
nano .bashrc
```
- Then a window will appear as the picture shows as follows. At the end of it type the following: 
![LD_LIBRARY_PATH_picture](/images/LD_LIBRARY_PATH_picture.png)
```bash
export LD_LIBRARY_PATH=/usr/local/lib/python3.8/dist-packages:$LD_LIBRARY_PATH
```
- After that type Ctrl+O, then Ctrl+X and in terminal the following:

```bash
# loading the .bashrc
source .bashrc
```
</p>

## 3. Installation process
<p align="justify">
You do not need to do anything for the installation, other than run a script where all the packages that are needed will be installed at the time the script is run.
</p>

### 3.1 Driver library
- Clone the repo in your home folder 
- Go to the "CiA402DevicePython" folder, open a terminal there and type:
```bash
# giving the permissions to the script to be executed
sudo chmod +x scriptSwig.sh

# execute the script
sh scriptSwig.sh
```
- Verify that the modules have been installed
```bash
# execute Python on terminal
python3 

# import PortBase or SocketCanPort modules (for example)
>>> import PortBase 
>>> import SocketCanPort 
```

### 3.2 Sensor library
- Go to the "SensorIntegrationPython" folder, open a terminal there and type:
```bash
# giving the permissions to the script to be executed
sudo chmod +x scriptSwig.sh

# execute the script
sh scriptSwig.sh
```
- Verify that the modules have been installed
```bash
# execute Python on terminal
python3 

# import imu3dmgx510 module (for example)
>>> import imu3dmgx510
```

## 4. Using the libraries in an IDE
<p align="justify">
Only Qt creator had been used for the management of the libraries. To make it worked, we had to perform a series of steps so that the library could be executed in the IDE (just for moving a soft robotic articulation). However, recently VS Code has been used and no further steps are required apart from opening the project in the IDE. 
</p>

If you want to use specifically Qt Creator, here is a user's guide to configure it correctly:


*Now you can start using the library in Python*


