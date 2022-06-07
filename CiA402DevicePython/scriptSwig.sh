#!/bin/bash

  echo Script for create files .so
  sleep 1s
  cd PythonProject/DriversPython/CiA402DevicePython
  
  sudo apt-get update
  sudo apt-get install python3.8.10
  sudo apt-get install python3-distutils --reinstall
  sudo apt-get install python3-dev
  sudo apt-get install cython3
  sudo apt-get install swig
  sudo apt-get install g++
  
  swig -c++ -python PortBase.i
  python3 setupPortBase.py build_ext --inplace
  
  swig -c++ -python SocketCanPort.i
  python3 setupSocketCanPort.py build_ext --inplace
  
  swig -c++ -python CiA301CommPort.i
  python3 setupCiA301CommPort.py build_ext --inplace
  
  swig -c++ -python CiA402SetupData.i
  python3 setupCiA402SetupData.py build_ext --inplace
  
  swig -c++ -python Cia402device.i
  python3 setupCia402device.py build_ext --inplace
  
  
  sudo mv PortBase.py /usr/local/lib/python3.10/dist-packages
  sudo mv SocketCanPort.py /usr/local/lib/python3.10/dist-packages
  sudo mv CiA301CommPort.py /usr/local/lib/python3.10/dist-packages
  sudo mv CiA402SetupData.py /usr/local/lib/python3.10/dist-packages
  sudo mv Cia402device.py /usr/local/lib/python3.10/dist-packages

  sudo mv _PortBase.so /usr/local/lib/python3.10/dist-packages
  sudo mv _SocketCanPort.so /usr/local/lib/python3.10/dist-packages
  sudo mv _CiA301CommPort.so /usr/local/lib/python3.10/dist-packages
  sudo mv _CiA402SetupData.so /usr/local/lib/python3.10/dist-packages
  sudo mv _Cia402device.so /usr/local/lib/python3.10/dist-packages
  
  
  
  


