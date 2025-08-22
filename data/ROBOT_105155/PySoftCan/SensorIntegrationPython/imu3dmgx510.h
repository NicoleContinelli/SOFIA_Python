#ifndef IMU3DMGX510_HPP
#define IMU3DMGX510_HPP

#define CAL_LOOPS 5 //number of initial calibration attempts
#define T_OUT 1000*3000 //useconds
#define T_WAIT 1000*100 //useconds

#include <iostream>
#include <sstream>
#include <string>
#include <math.h>
#include "attitude_estimator.h"
#include <tuple>
#include <boost/algorithm/hex.hpp>
using namespace boost::algorithm;

#include "SerialComm.h"
using namespace std;
using namespace stateestimation;
//using namespace std::string_literals;
//using std::string_literals::operator""s;

class IMU3DMGX510
{

public:

    IMU3DMGX510(string portName = "/dev/ttyUSB0", int new_freq = 100); //Constructor

     // -------- Initialization of the IMU. Implementation in imu3dmgx510.cpp --------

    bool check(); //This funcion checks if our imu is active
    bool set_freq(int); //This funcion will set the freq of our IMU
    long calibrate(); //This func will get initial offsets to correct future measures

     // -------- Configuration of the IMU. Implementation in imu3dmgx510.cpp --------

    long Ping();
    long set_IDLEmode();  //This function sets our device into IDLE mode
    long set_streamon(); //This function enable stream
    long set_streamoff(); //This function disable stream
    long set_reset(); //This function resets the device
    long set_devicetogetgyroacc(); //This function configure our device to give us gyro(x,y,z) and acc(x,y,z)
    long set_devicetogetgyro(); //This function configure our device to give us gyro(x,y,z)

    // -------- Getting data of the IMU (Polling and Streaming). Implementation in imu3dmgx510.cpp --------

    std::tuple <float, float, float> get_gyroPolling();
    double* get_euleranglesPolling();

    long GetPitchRoll(double & pitch, double & roll);
    double* GetPitchRollYaw(double & pitch, double & roll, double & yaw, double angles[]);
    double GetPitch(double pitch, double roll, double yaw);
    double GetRoll(double pitch, double roll, double yaw);
    double GetYaw(double pitch, double roll, double yaw);
    long Reset();

   //This methods are developed to plot specified numbres of samples on Matlab
    //We will get a vector to be copy pasted in Matlab to plot it
    std::tuple <double*,double*,double*> get_gyroStreaming (int); //This funcion gives us gyro data
    std::tuple <double*,double*,double,double> get_euleranglesStreaming (int); //This funcion gives us pitch and roll, and both initial pitch offset and initial roll offset

    //Both following methods are done to make our imu start sending data
    //They can be included in a loop
    double* EulerAngles();
    double* GyroData();

private: //Attributes

    string portResponse;
    long comprobacion;
    int firsttime=0;
    long charsWritten=0;


    union ulf
    {
        unsigned long ul;
        float f;
    };

    SerialComm port; //DO NOT try to invoce the constructor here
    AttitudeEstimator estimador;

    //Initial offset
    double rolloffset;
    double pitchoffset;
    double yawoffset;

    double true_yawoff;//CR

    double tmpYaw;

//    //Setting of GyroBias
//    double bx = -0.002786;
//    double by = -0.001833;
//    double bz = -0.001066;
    //Setting of GyroBias
    double bx = -0.002681;
    double by = -0.002166;
    double bz = -0.001784;

    //Defaults gains used
    double Kp = 2.2;
    double Ti = 2.65;
    double KpQuick = 10;
    double TiQuick = 1.25;

    //Frequency of our imu
    double freq;
    double period;

    //Using string literals need a c++14 or higher.
    //Find an alternative if lower c++ standard is needed.
    //Specific data packets used by IMU3DMGX510
    string ping = ("\x75\x65\x01\x02\x02\x01\xE0\xC6");
    string ok_ping = string("\x75\x65\x01\x04\x04\xF1\x01\x00\xD5\x6A"s);

    std::string idle = "\x75\x65\x01\x02\x02\x02\xe1\xc7";
    string ok_idle = ("\x75\x65\x01\x04\x04\xF1\x02\x00\xD6\x6C"s);
//    string ok_idle = ("\x75\x65\x01\x04\x04\xF1\x02\x00"s);
    std::string imudata1 = "\x75\x65\x0c\x07\x07\x08\x01\x01\x05\x03\xe8\xee\x04"s;
    std::string imudata100 = ("\x75\x65\x0c\x07\x07\x08\x01\x01\x05\x00\x0a\x0d\x20"s);
    std::string imudata1000 = ("\x75\x65\x0c\x07\x07\x08\x01\x01\x05\x00\x01\x04\x17"s);
    std::string reset = "\x75\x65\x01\x02\x02\x7e\x5d\x43"s;
    std::string ok_reset = ("\x75\x65\x01\x04\x04\xF1\x7e\x00\x52\x64"s);
    std::string baudratenew = ("\x75\x65\x0c\x07\x07\x40\x01\x00\x03\x84\x00\xbc\x64"s);
    std::string gyracc1 = ("\x75\x65\x0c\x0a\x0a\x08\x01\x02\x04\x03\xe8\x05\x03\xe8\xe4\x0b"s);
    std::string gyracc50 = ("\x75\x65\x0c\x0a\x0a\x08\x01\x02\x04\x00\x14\x05\x00\x14\x36\xd2"s);
    std::string gyracc100 = ("\x75\x65\x0c\x0a\x0a\x08\x01\x02\x04\x00\x0a\x05\x00\x0a\x22\xa0"s);
    std::string gyracc500 = ("\x75\x65\x0c\x0a\x0a\x08\x01\x02\x04\x00\x02\x05\x00\x02\x12\x78"s);
    std::string gyracc1000 = ("\x75\x65\x0c\x0a\x0a\x08\x01\x02\x04\x00\x01\x05\x00\x01\x10\x73"s);
    std::string setok = ("\x75\x65\x0c\x04\x04\xF1\x08\x00\xE7\xBA"s);
    std::string streamon = "\x75\x65\x0c\x05\x05\x11\x01\x01\x01\x04\x1a"s;
    std::string streamoff = ("\x75\x65\x0c\x05\x05\x11\x01\x01\x00\x03\x19"s);
    std::string ok_streamon = ("\x75\x65\x0c\x04\x04\xF1\x11\x00\xf0\xcc"s);
    std::string polling = ("\x75\x65\x0c\x04\x04\x01\x00\x00\xef\xda"s);
    std::string poll_ready = ("\x75\x65\x0c\x04\x04\xF1\x01\x00\xe0\xac"s);
    std::string poll_data = ("\x75\x65\x80\x1c");

    //comm variables
    uint descriptor;
    uint payload;

    //methods
    ///
    /// \brief GetPortLine: Get one line of data from the sensor
    /// \param portLine(out): the line read.
    /// \return : Size of the line.
    ///
    long GetPortLine(string & portLine);

    long FindPortLine(string findText, string & wholeLine);

    long ReadACK(string expected);
    long ShowCode(string showString);
};

#endif // IMU3DMGX510_HPP

