  #!/bin/bash

  echo Script for create files .so
  sleep 1s
  cd PythonProject/SensorIntegrationPython
  
  sudo apt-get update
  sudo apt-get install python3.8.10
  sudo apt-get install python3-distutils --reinstall 
  sudo apt-get install python3-dev
  sudo apt-get install python3-pip
  sudo pip install cython
  sudo apt-get install swig
  sudo apt-get install libboost-all-dev
  sudo apt-get install g++
  sudo chmod a+rw /dev/ttyUSB0
  
  swig -c++ -python SerialComm.i
  python3 setupSerialComm.py build_ext --inplace
  
  swig -c++ -python attitude_estimator.i
  python3 setupattitude_estimator.py build_ext --inplace
  
  echo Deleting temporarly the private variables to create the modules

  echo swig -c++ -python imu3dmgx510.i
  echo python3 setupimu3dmgx510.py build_ext --inplace
  
  sudo cp SerialComm.py /usr/local/lib/python3.10/dist-packages
  sudo cp attitude_estimator.py /usr/local/lib/python3.10/dist-packages
  sudo cp imu3dmgx510.py /usr/local/lib/python3.10/dist-packages

  sudo cp _SerialComm.so /usr/local/lib/python3.10/dist-packages
  sudo cp _attitude_estimator.so /usr/local/lib/python3.10/dist-packages
  sudo cp _imu3dmgx510.so /usr/local/lib/python3.10/dist-packages
