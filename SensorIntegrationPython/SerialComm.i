%module SerialComm

%{
#include "/usr/include/boost/asio.hpp"
#include "/usr/include/boost/asio/serial_port.hpp"
#include "SerialComm.h"
%}

%include "/usr/include/boost/asio.hpp"
%include "/usr/include/boost/asio/serial_port.hpp"
%include "SerialComm.h"
