%module imu3dmgx510
%import "SerialComm.i"
%import "attitude_estimator.i"
%include "stdint.i"
%include "typemaps.i"
%include <std_string.i>

%{
#include "/usr/include/boost/algorithm/hex.hpp"
#include "imu3dmgx510.h"
%}

%include "/usr/include/boost/algorithm/hex.hpp"
%include "imu3dmgx510.h"

