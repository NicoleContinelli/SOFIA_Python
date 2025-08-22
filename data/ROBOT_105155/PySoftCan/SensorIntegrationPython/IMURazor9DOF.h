#ifndef IMUSPARKFUNRAZOR9DOF_H
#define IMUSPARKFUNRAZOR9DOF_H

#include "SerialComm.h"
#include "attitude_estimator.h"

using namespace stateestimation;

class IMURazor9DOF : public SerialComm
{
public:
    IMURazor9DOF(string portName = "/dev/ttyUSB0");

    long GetPitchRollYaw(double dts, double & o_pitch, double & o_roll, double & o_yaw);
    long GetYawPitchRoll(double dts, double & o_yaw, double & o_pitch, double & o_roll);

private:
    AttitudeEstimator att;
    //Setting of GyroBias
    double bx = -0.002681;
    double by = -0.002166;
    double bz = -0.001784;

    //Defaults gains used
    double Kp = 2.2;
    double Ti = 2.65;
    double KpQuick = 10;
    double TiQuick = 1.25;

    string line;
    string tmp;
    long p0,p1;

    double gam[9]; //Gyroscope, accelerometer and magnetometer data
};

#endif // IMUSPARKFUNRAZOR9DOF_H
