#ifndef CIA402DEVICE_H
#define CIA402DEVICE_H

#include <chrono>
#include <thread>
#include <math.h>

#include "CiA301CommPort.h"
#include "SocketCanPort.h"
#include "ObjectDictionary.h"
#include "PortBase.h"
#include "CiA402SetupData.h"

#define PI 3.14159265358
#define RPM2RADS (2.0*PI)/60.0
#define RADS2RPM 60.0/(2.0*PI)
#define DEG2RADS (2.0*PI)/360.0
#define RADS2DEG 360.0/(2.0*PI)

/*
 * If no factor is applied, the profile velocity object receives data
 * as a FIXED32 variable. The high part represents encoder
 * increments/sample, and the low part represents a subdivision
 * of an increment.
 *
 * 65536 (0x00010000) = 1 encoder increment/sample.
 * The minimum speed is 1 encoder increment/sample.
 */
#define HIGHPART_BITSHIFT_16 0x10000

#define ANALOGUE_INPUT_SCALE 0xFFF0


class CiA402Device : public CiA301CommPort
{
public:

    // =========================================================
    // Constructors
    // =========================================================

    CiA402Device();
    CiA402Device(uint8_t new_id);
    CiA402Device(uint8_t new_id, int fdPort);
    CiA402Device(uint8_t new_id, PortBase *new_port);
    CiA402Device(uint8_t new_id,
                 PortBase *new_port,
                 CiA402SetupData *deviceData);


    // =========================================================
    // Node / State Machine
    // =========================================================

    long Reset();
    long StartNode();

    long SwitchOn();
    long SwitchOff();
    long ForceSwitchOff();
    long QuickStop();


    // =========================================================
    // Status / Errors
    // =========================================================

    uint16_t CheckStatus();
    void PrintStatus();
    int CheckError();

    uint16_t GetStatus();
    int GetOperationMode();

    // =========================================================
    // Operation Mode
    // =========================================================

    long OperationMode(const vector<uint8_t> new_mode);

    long SetupPositionMode(
        const uint32_t velocity = 1,
        const uint32_t acceleration = 1
    );

    long Setup_Velocity_Mode(
        const uint32_t acceleration = 1,
        const uint32_t target = 0
    );

    long Setup_Torque_Mode(uint32_t torque_slope = 1000);


    // =========================================================
    // Motion Commands
    // =========================================================

    long SetPosition(double target);
    long SetVelocity(double target);
    long SetTorque(double target);


    // =========================================================
    // Enable / Disable
    // =========================================================

    long EnableTorque();
    long DisableTorque();


    // =========================================================
    // Feedback
    // =========================================================

    double GetPosition();
    double GetVelocity();
    double GetVelocityTP();
    double GetFilteredVelocity(int samples);
    double GetMeanVelocity();

    double GetAmps();
    double GetFilterdAmps();


    // =========================================================
    // Communication
    // =========================================================

    long SetCommunications(int fdPort);


    // =========================================================
    // Encoder
    // =========================================================

    long ResetEncoderPosition();


    // =========================================================
    // Configuration
    // =========================================================

    long SetEnc_res(int lines);
    long SetRed_Mot(float reduction_ratio);
    long SetSampling_period(float sampling_period);


private:

    // =========================================================
    // Initialization
    // =========================================================

    long Init(CiA402SetupData *deviceData);


    // =========================================================
    // Communication / Device Configuration
    // =========================================================

    int comm;


    // =========================================================
    // Motor / Encoder Configuration
    // =========================================================

    float reduction_ratio_motor;
    int encoder_resolution;
    float SampSL;

    double motorCurrentLimit;
    double driverCurrentLimit;


    // =========================================================
    // Scaling Factors
    // =========================================================

    float Scaling_Factors_Velocity;
    float Scaling_Factors_Position;
    float Scaling_Factors_Acceleration;


    // =========================================================
    // Current / Torque Variables
    // =========================================================

    double targetCurrent;
    int32_t targetCurrentIU;


    // =========================================================
    // GetMeanVelocity Variables
    // =========================================================

    double currentPosition;
    double lastPosition;
    double currentPoss;
    double previousPoss;

    double meanVelocity;

    std::chrono::system_clock::time_point actualTimeValue;
    std::chrono::system_clock::time_point lastTimeValue;
    std::chrono::system_clock::time_point encoderChangeTime;

    double encoderSpan;


    // =========================================================
    // GetVelocityTP Variables
    // =========================================================

    std::chrono::system_clock::time_point currentTime;
    std::chrono::system_clock::time_point previousTime;

    std::chrono::nanoseconds dtsWait;
    std::chrono::nanoseconds tWaited;
};


#endif // CIA402DEVICE_H