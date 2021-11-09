#!/bin/bash

  echo Script for initialize the CAN communication
  sleep 1s
  cd PythonProject/DriversPython/CiA402DevicePython
  
  sudo ip link set can1 type can bitrate 1000000
  sudo ifconfig can1 up
  sudo candump can1 
  
  
	
  
  
  
  
  


