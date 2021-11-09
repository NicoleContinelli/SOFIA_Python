%module CiA301CommPort
%include <std_string.i>
%include "stdint.i"
%include "typemaps.i"
%import "PortBase.i"
%ignore tx0;
%ignore rx0;

%{
#include "CiA301CommPort.h"
%}

%ignore  ReadSDO(vector<uint8_t> address, int subindex);  
%include "CiA301CommPort.h"
