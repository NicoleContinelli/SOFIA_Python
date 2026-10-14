#include "Cia402device.h"

vector<uint8_t> data32to4x8(uint32_t in);

vector<uint8_t> data16to2x8(uint16_t in);

// ============================================================
// Initialization
// ============================================================

long CiA402Device::Init(CiA402SetupData *deviceData)
{


    Scaling_Factors_Position = deviceData->getScaling_Factors_Position();
    Scaling_Factors_Velocity = deviceData->getScaling_Factors_Velocity();
    Scaling_Factors_Acceleration= deviceData->getScaling_Factors_Acceleration();

    motorCurrentLimit = deviceData->GetMotorCurrentLimit();
    driverCurrentLimit = deviceData->GetDriverCurrentLimit();

    //Initialize velocity and position
    encoder_resolution = deviceData->getEncRes();
    meanVelocity = 0;
    currentPosition = 0;
    lastPosition = 0;
    encoderSpan = 0;

    tWaited = chrono::milliseconds(1);

    //initialize variables for GetVelocityTP
    currentPoss = 0;
    previousPoss = 0;
    previousTime = std::chrono::system_clock::now();

    ///set adress for filtered amps (not working)
//    const vector<uint8_t> cutoff = {0xFF,0xFF};
//    WriteSDO(od::filtered_amps_set_cutoff,cutoff);

//    lastTimeValue = actualTimeValue;
//    actualTimeValue = chrono::system_clock::now();
//    tWaited = actualTimeValue.time_since_epoch() - lastTimeValue.time_since_epoch(); //nanoseconds
//    tWaited = tWaited/1000000; //seconds


//    //Scaling();
//    float count_sec = encoder_resolution/60.0;
//    // Motor_Position[IU]=Scaling_factors_velocity*Load_Position[SI]
//    Scaling_Factors_Position = reduction_ratio_motor*encoder_resolution/(2.0*PI);

//    // Motor_Speed[IU]=Scaling_factors_velocity*Load_Speed[SI]
//    Scaling_Factors_Velocity = RADS2RPM*count_sec*reduction_ratio_motor*SampSL;
//    cout << "Scaling_Factors_Velocity - " << Scaling_Factors_Velocity << endl;

//    // Motor_Accel[IU]=Scaling_factors_velocity*Load_Accel[SI]
//    Scaling_Factors_Acceleration = Scaling_Factors_Velocity*SampSL;


    return 0;
}

// ============================================================
// Constructors
// ============================================================

CiA402Device::CiA402Device()
    : CiA301CommPort(1,1)
{
    CiA402SetupData defaultInit(2048,24,0.001, 0.144, 20 );
    Init(&defaultInit);
    comm = 1;

}

CiA402Device::CiA402Device(uint8_t new_id)
    : CiA301CommPort(1, new_id)
{
    CiA402SetupData defaultInit(2048,24,0.001, 0.144, 20 );
    Init(&defaultInit);
    comm = 1;
}

CiA402Device::CiA402Device(uint8_t new_id, int fdPort)
    : CiA301CommPort(fdPort, new_id)
{

    CiA402SetupData defaultInit(2048,24,0.001, 0.144, 20 );
    Init(&defaultInit);
    comm = fdPort;

}

CiA402Device::CiA402Device(uint8_t new_id, PortBase *new_port)
    : CiA301CommPort(new_port, new_id)
{
    CiA402SetupData defaultInit(2048,24,0.001, 0.144, 20 );
    Init(&defaultInit);

}

CiA402Device::CiA402Device(uint8_t new_id, PortBase *new_port, CiA402SetupData *deviceData)
    : CiA301CommPort(new_port, new_id)
{
     Init(deviceData);
//     port=new_port;


}

// ============================================================
// Node / State Machine
// ============================================================

long CiA402Device::Reset()
{

//     double response;
     //response = WriteNMT(od::reset);
     cout<<"RESET id: " << (uint)id << endl;

     WriteNMT(od::fullreset);


     //Wait Start finish NMT [01 id]
     //ReadNMT(nmt::started);

     //reset response 700+id -->booting
     ReadErrorNMT();
     //Wait needed for reset to finish. Using sleep
     sleep(1);

     WriteNMT(od::start);

     cout<<"NODE " << (uint)id << " STARTED"<<endl;

     FlushBuffer();
return 0;
}

long CiA402Device::StartNode()
{

     cout<<"START NODE"<<endl;
     WriteNMT(od::start);
     return 0;

}

long CiA402Device::SwitchOn()
{
    EnablePDOs();
    FlushBuffer();

    long response;

    // --------------------------------------------------
    // 1. Ready to switch on
    // --------------------------------------------------
    cout << "GOREADYTOSWITCHON" << endl;

    response = WritePDO1(od::goreadytoswitchon);

    if (response != 0)
    {
        cerr << "ERROR: Failed to send Ready-to-Switch-On"
             << endl;

        DisablePDOs();
        FlushBuffer();
        return -1;
    }

    response = ReadPDO(1);
    FlushBuffer();

    cout << "READYTOSWITCHON RESPONSE: "
         << response << endl;


    // --------------------------------------------------
    // 2. Switch on
    // --------------------------------------------------
    response = WritePDO1(od::goswitchon);

    if (response != 0)
    {
        cerr << "ERROR: Failed to send Switch-On"
             << endl;

        DisablePDOs();
        FlushBuffer();
        return -1;
    }

    response = ReadPDO(1);
    FlushBuffer();


    // --------------------------------------------------
    // 3. Enable operation
    // --------------------------------------------------
    response = WritePDO1(od::goenable);

    if (response != 0)
    {
        cerr << "ERROR: Failed to enable operation"
             << endl;

        DisablePDOs();
        FlushBuffer();
        return -1;
    }

    cout << "NODE "
         << (uint)id
         << " ENABLED"
         << endl;

    DisablePDOs();


    // --------------------------------------------------
    // 4. Wait for drive stabilization
    // --------------------------------------------------
    sleep(1);


    // --------------------------------------------------
    // 5. Read statusword
    // --------------------------------------------------
    uint16_t status = CheckStatus();

    cout << "6041h after SwitchOn = 0x"
         << hex
         << status
         << dec
         << endl;


    // --------------------------------------------------
    // 6. Wait before next SDO transaction
    // --------------------------------------------------
    sleep(1);

    FlushBuffer();

    return 0;
}

long CiA402Device::ForceSwitchOff(){
    WritePDO1(od::goswitchondisable);
    return 0;
}

long CiA402Device::SwitchOff()
{
    uint16_t status;
    status=CheckStatus();
    //filter state
    status = status&0x6f; //mask 01101111=6f

    switch(status)
    {
    case 0x21:
        cout<<"7"<<endl;
        WritePDO1(od::quickstop);
        FlushBuffer();
        break;
    case 0x23:
        cout<<"10"<<endl;
        //WritePDO(od::readytoswitchon);
            WritePDO1(od::quickstop);
        FlushBuffer();
        break;
    case 0x27:
        cout<<"Leaving Operation enabled"<<endl;
        cout<<"11"<<endl;
        WritePDO1(od::quickstop);
        FlushBuffer();
        cout<<"12"<<endl;
        WriteNMT(od::start);
        break;
    case 0x07:
        cout<<"5"<<endl;
        WritePDO1(od::quickstop);
        FlushBuffer();
        break;
    case 0x0f:
    case 0x2f:
        cout<<"Fault reaction active"<<endl;
        break;
    case 0x08:
    case 0x28:
        cout<<"Fault"<<endl;
        break;
    default:
        cout<<"Not known"<<endl;

    }
    return 0;
}

long CiA402Device::QuickStop()
{
    const vector<uint8_t> mode = {0x00};
    WriteSDO(od::quick_stop_mode,mode);
    sleep(1);
    WriteSDO(od::stop_option_code,mode);
    sleep(1);
    cout<<"SwitchOff"<<endl;
    WritePDO1(od::quickstop);
    FlushBuffer();

    return 0;
}

// ============================================================
// Operation Mode
// ============================================================

long CiA402Device::OperationMode(const vector<uint8_t> new_mode)
{
    long requested_mode = new_mode[0];

    // Write requested operation mode to 6060h
    long write_response =
        WriteSDO(od::OperationMode, new_mode);

    if (write_response != 0)
    {
        cout << "ERROR: Failed to write Operation Mode (6060h)." << endl;
        return -1;
    }

    // --------------------------------------------------
    // Wait for Operation Mode Display (6061h)
    // --------------------------------------------------

    const int max_attempts = 20;
    const int wait_ms = 100;

    long mode_after = -1;

    for (int i = 0; i < max_attempts; i++)
    {
        usleep(wait_ms * 1000);

        mode_after =
            ReadSDO(od::OperationModeDisplay);

        if (mode_after == requested_mode)
        {
            cout << "Operation Mode configured." << endl;
            return 0;
        }
    }

    // --------------------------------------------------
    // Requested mode was not reached
    // --------------------------------------------------

    cout << "ERROR: Operation Mode configuration failed." << endl;
    cout << "Requested mode = " << requested_mode << endl;
    cout << "Actual mode    = " << mode_after << endl;

    return -1;
}

// ============================================================
// Status / Errors
// ============================================================

uint16_t CiA402Device::CheckStatus()
{
    uint16_t status;
    vector<uint8_t> data = od::statusword;
//    data.push_back(od::statusword[0]);
//    data.push_back(od::statusword[1]);

    //Ask for the status word
    status = (uint16_t) ReadSDO(data);
    //status = 0x07;
    //filter state

    return status;

}

uint16_t CiA402Device::GetStatus()
{
    return static_cast<uint16_t>(ReadSDO(od::statusword));
}


int CiA402Device::GetOperationMode()
{
    return static_cast<int>(ReadSDO(od::OperationModeDisplay));
}

void CiA402Device::PrintStatus()
{
   uint16_t status;
    //vector<uint8_t> data={0x40};
    vector<uint8_t> data=od::statusword;
//    data.push_back(od::statusword[0]);
//    data.push_back(od::statusword[1]);

    //Ask for the status word
    status = (uint16_t) ReadSDO(data);
    cout << "status word: " << std::bitset<16>(status)<< endl;

//    status = 0x024; //testing data
    //filter state
    status &= 0x6f; //mask 01101111=6f

    switch(status)
    {
    case 0x00:
        cout<<"Not Ready to switch on"<<endl;
        break;
    case 0x60:
    case 0x40:
        cout<<"Switch on disabled"<<endl;
        break;
    case 0x21:
        cout<<"Ready to switch on"<<endl;
        break;
    case 0x23:
        cout<<"Switched on"<<endl;
        break;
    case 0x27:
        cout<<"Operation enabled"<<endl;
        break;
    case 0x07:
        cout<<"Quick stop active"<<endl;
        break;
    case 0x0f:
    case 0x2f:
        cout<<"Fault reaction active"<<endl;
        break;
    case 0x08:
    case 0x28:
        cout<<"Fault"<<endl;
        break;
    default:
        cout<<"Not known"<<endl;

    }
   return;
}

int CiA402Device::CheckError()
{
    uint32_t error;
    vector<uint8_t> data={0x40};
    data.push_back(od::checkerror[0]);
    data.push_back(od::checkerror[1]);

    //Ask for the status word
    error = (uint32_t) ReadSDO(data);

    cout << "checkerror: " << error << endl;
    cout << "checkerror: " << std::bitset<32>(error)<< endl;
    //Print decoded response for status word
    switch (error)
    {

    case 1: //
        break;

    }

    return 0;
}

// ============================================================
// Mode Configuration
// ============================================================

long CiA402Device::SetupPositionMode(const uint32_t velocity,const uint32_t acceleration)
{
    int32_t velocityr;
    int32_t accelerationr;

    cout << "========================================" << endl;
    cout << "SET POSITION MODE" << endl;
    cout << "========================================" << endl;

    // ==================================================
    // 1. Select Position Profile Mode
    // ==================================================

    long mode_result =
        OperationMode(od::positionmode);

    if (mode_result != 0)
    {
        cout << "ERROR: Drive did NOT enter Position Mode!"
             << endl;

        return -1;
    }

    // ==================================================
    // 2. Profile velocity
    // ==================================================

    velocityr =
        (int32_t)(
            (velocity * Scaling_Factors_Velocity)
            * HIGHPART_BITSHIFT_16
        );

    long response_vel =
        WriteSDO(
            od::profile_velocity,
            data32to4x8(velocityr)
        );

    if (response_vel != 0)
    {
        cout << "ERROR writing 6081h." << endl;
        return -1;
    }

    // ==================================================
    // 3. Profile acceleration
    // ==================================================

    accelerationr =
        (int32_t)(
            (acceleration * Scaling_Factors_Acceleration)
            * HIGHPART_BITSHIFT_16
        );

    long response_acc =
        WriteSDO(
            od::profile_acceleration,
            data32to4x8(accelerationr)
        );

    if (response_acc != 0)
    {
        cout << "ERROR writing 6083h." << endl;
        return -1;
    }

    cout << "Position Profile Mode configured." << endl;

    return 0;
}

long CiA402Device::Setup_Velocity_Mode(const uint32_t acceleration,const uint32_t target)
{
    int32_t target_velocity_r;
    int32_t acceleration_r;

    cout << "========================================" << endl;
    cout << "SET VELOCITY MODE" << endl;
    cout << "========================================" << endl;

    // ==================================================
    // 1. Select Velocity Profile Mode
    // ==================================================

    long mode_result =
        OperationMode(od::velocitymode);

    if (mode_result != 0)
    {
        cout << "ERROR: Drive did NOT enter Velocity Mode!"
             << endl;

        return -1;
    }

    // ==================================================
    // 2. Target Velocity
    // ==================================================

    target_velocity_r =
        (int32_t)(
            (target * Scaling_Factors_Velocity)
            * HIGHPART_BITSHIFT_16
        );

    long response_vel =
        WriteSDO(
            od::target_velocity,
            data32to4x8(target_velocity_r)
        );

    if (response_vel != 0)
    {
        cout << "ERROR writing Target Velocity." << endl;
        return -1;
    }

    // ==================================================
    // 3. Profile Acceleration
    // ==================================================

    acceleration_r =
        (int32_t)(
            (acceleration * Scaling_Factors_Acceleration)
            * HIGHPART_BITSHIFT_16
        );

    long response_acc =
        WriteSDO(
            od::profile_acceleration,
            data32to4x8(acceleration_r)
        );

    if (response_acc != 0)
    {
        cout << "ERROR writing Profile Acceleration (6083h)."
             << endl;
        return -1;
    }

    // ==================================================
    // Configuration completed
    // ==================================================

    cout << "Velocity Profile Mode configured." << endl;

    return 0;
}

long CiA402Device::Setup_Torque_Mode(uint32_t torque_slope)
{
    cout << "========================================" << endl;
    cout << "SET TORQUE MODE" << endl;
    cout << "========================================" << endl;


    // ==================================================
    // 1. Select Profile Torque Mode
    //    6060h = 04
    // ==================================================

    long mode_result = OperationMode(od::torquemode);

    if (mode_result != 0)
    {
        cout << "ERROR: Drive did NOT enter Profile Torque Mode!"
             << endl;

        return -1;
    }

    cout << "Profile Torque Mode selected." << endl;


    // ==================================================
    // 2. Configure Torque Slope
    //    6087h = torque slope
    //
    //    Default value:
    //    1000 = 100% of motor rated current per second
    //
    //    With 6075h = 823 mA:
    //    1000 -> 0.823 A/s
    //
    //    Examples:
    //     500 -> 0.4115 A/s
    //     200 -> 0.1646 A/s
    // ==================================================

    long response_slope =
        WriteSDO(
            od::torque_slope,
            data32to4x8(torque_slope)
        );

    if (response_slope != 0)
    {
        cout << "ERROR writing Torque Slope (6087h)."
             << endl;

        return -1;
    }

    cout << "Torque Slope configured: "
         << torque_slope
         << endl;


    // ==================================================
    // 3. Configuration completed
    // ==================================================

    cout << "Profile Torque Mode configured." << endl;

    return 0;
}

// ============================================================
// Motion Commands
// ============================================================

long CiA402Device::SetPosition(double target){


    long retval;

    //Why is this needed?
    WritePDO1(od::goenable);

    //convert target to internal units value
    long target_t=(long)(target*Scaling_Factors_Position);

    //Write the IU target value in dictionary
    retval = WriteSDO(od::target_position,data32to4x8(target_t));
//    long stat = ReadSDO(od::statusword);
    //sleep(1);

    //Send control word to update the system
    // ipos manual page 149
    //bits: 6=0(absolute) 5=1(immediatly) 4=1(update)
    vector<uint8_t>cw={0x3F,0x00};
    WritePDO1(cw);
    return 0;//stat;
}

long CiA402Device::SetVelocity(double target){


    int32_t targetr;

    double ui = target*Scaling_Factors_Velocity;

    if( ui < 1 && ui > 0)
        ui = HIGHPART_BITSHIFT_16;
    else if( ui > - 1 && ui < 0)
        ui = - HIGHPART_BITSHIFT_16;
    else if ( ui == 0)
        ui = 0;
    else
        ui = ui * HIGHPART_BITSHIFT_16;

    int32_t t = (int32_t)ui;
    WriteSDO(od::target_velocity,data32to4x8(t));

    // Motor_Velocity[IU]=Scaling_factors_velocity*Load_Velocity[SI]
    return 0;
}

long CiA402Device::SetTorque(double target)
{
    cout << "========================================" << endl;
    cout << "SET TORQUE" << endl;
    cout << "========================================" << endl;

    // ==================================================
    // 1. Limit normalized torque command
    // ==================================================

    if (target > 1.0)
        target = 1.0;
    else if (target < -1.0)
        target = -1.0;


    // ==================================================
    // 2. Convert normalized command to Target Torque
    //
    // 6071h = Target Torque
    // INTEGER16
    //
    // 1000 = 100% of motor rated current
    //  500 =  50%
    //  100 =  10%
    // -100 = -10%
    // ==================================================

    int16_t target_torque =
        static_cast<int16_t>(
            std::lround(target * 1000.0)
        );


    cout << "Target torque 6071h = "
         << target_torque
         << " (" << target * 100.0 << "%)"
         << endl;


    // ==================================================
    // 3. Write Target Torque (6071h)
    // ==================================================

    long response =
        WriteSDO(
            od::target_torque,
            data16to2x8(
                static_cast<uint16_t>(target_torque)
            )
        );

    if (response != 0)
    {
        cerr << "ERROR writing Target Torque (6071h)."
             << endl;

        return -1;
    }


    // ==================================================
    // 4. Execute Torque Profile
    //    Controlword = 0x001F
    // ==================================================

    response = WritePDO1(od::torque_run);

    if (response != 0)
    {
        cerr << "ERROR sending Torque RUN controlword."
             << endl;

        return -1;
    }


    return 0;
}

// ============================================================
// Enable / Disable
// ============================================================

long CiA402Device::EnableTorque(){
     long response;
     FlushBuffer();
     response = WritePDO1(od::goswitchon);
     response = WritePDO1(od::goenable);
     cout<<"Node " << (uint)id <<" enabled"<<endl;
     //sleep(1);
     FlushBuffer();
    return 0;
}

long CiA402Device::DisableTorque(){
    //EnablePDOs();
    long response;
    response = WritePDO1(od::goswitchon);
    //response = ReadPDO(0);
    FlushBuffer();
    cout<<"Disabling torque"<<endl;
    //DisablePDOs();
    return 0;
}

// ============================================================
// Feedback
// ============================================================

double CiA402Device::GetPosition()
{
    int32_t position = (int32_t)ReadSDO(od::positionaddress);

    double scale_position =
        (double)position / (double)Scaling_Factors_Position;

    return scale_position;
}

double CiA402Device::GetVelocity()
{

    int32_t velocity= (int32_t)ReadSDO(od::velocityaddress);

    double scale_velocity = (double)velocity;
    scale_velocity = scale_velocity / ( (double)(Scaling_Factors_Velocity*HIGHPART_BITSHIFT_16) );
      // Motor_Position[IU]=Scaling_factors_velocity*Load_Position[SI];

//    cout << std::hex << "velocity  hex    - " <<  velocity <<endl;
//    cout << "velocity  float    - " << (double)velocity/(Scaling_Factors_Velocity*HIGHPART_BITSHIFT_16) << endl;
//    cout << "velocity           - " << velocity/(Scaling_Factors_Velocity*HIGHPART_BITSHIFT_16)<< endl;
//    cout << "velocity Low  - " << (velocity << 16) << endl;

    return scale_velocity;
}

double CiA402Device::GetVelocityTP() // Through Position
{
    currentTime = std::chrono::system_clock::now();
    std::chrono::duration<float,std::milli> duration = currentTime - previousTime;
    previousTime = currentTime;
    //printf("CurrentPoss: %f PreviousPoss: %f Duration: %f ", this->GetPosition(), previousPoss, duration.count()* 0.001);    
    currentPoss = this->GetPosition();
    double result = ( (currentPoss - previousPoss) / (duration.count()* 0.001) );
    previousPoss = currentPoss;
    return result;


}

double CiA402Device::GetMeanVelocity()
{

    int32_t position= (int32_t)ReadSDO(od::positionaddress);

//    cout<<"POS --- "<<position<<endl;
//    cout<<"reduction_ratio_motor*encoder_resolution "<<reduction_ratio_motor<< " "<<encoder_resolution<<" "<<reduction_ratio_motor*encoder_resolution<<endl;
    double scale_position = (double)position;

    lastPosition = currentPosition;
    currentPosition = scale_position / ( (double)Scaling_Factors_Position );

    if(lastPosition == currentPosition)
    {

        //keep old velocity value
        //check zero velocity
        if( chrono::system_clock::now() > encoderChangeTime)
        {
            meanVelocity = 0;
        }
    }
    else
    {
        //Compute velocity from position
        lastTimeValue = actualTimeValue;
        actualTimeValue = chrono::system_clock::now();
        tWaited = actualTimeValue.time_since_epoch() - lastTimeValue.time_since_epoch(); //nanoseconds
        tWaited = tWaited/1000000; //seconds
        meanVelocity = (currentPosition - lastPosition)/tWaited.count();
        //update zero check counter
        //that is, keeping actual velocity, prediction of the next encoder change
        encoderSpan = (2*M_PI/encoder_resolution)/meanVelocity;
        //time to check taking this encoder span
        encoderChangeTime = actualTimeValue + std::chrono::milliseconds(2*1000*long(encoderSpan));
    }
    cout << "meanVelocity =  " << meanVelocity <<  ", currentPosition =  " << currentPosition <<  ", lastPosition =  " << lastPosition <<endl;
    cout << "tWaited =  " << tWaited.count() <<endl;


    return meanVelocity;


}

double CiA402Device::GetFilteredVelocity(int samples)
{

    return 0;
}

double CiA402Device::GetAmps()
{
    double currentIU= (double)ReadSDO(od::getamps);

    double targetCurrent = (currentIU * 2.0 * driverCurrentLimit) / ANALOGUE_INPUT_SCALE * HIGHPART_BITSHIFT_16;

    return targetCurrent;
}

double CiA402Device::GetFilterdAmps()
{
    ///does not work yet

    int16_t amps= (int16_t)ReadSDO(od::filtered_amps);
    cout<<"Lectura int32 : "<<amps<<endl;
    double scaledamps = (double)amps;
    return scaledamps;
}

// ============================================================
// Communication
// ============================================================

long CiA402Device::SetCommunications(int fdPort)
{
    comm = fdPort;
    return 0;
}

// ============================================================
// Encoder
// ============================================================

long CiA402Device::ResetEncoderPosition()
{
    // Object 2081h:00 → Set Actual Position (INTEGER32)
    // This resets: actual, target, demanded positions.

    std::vector<uint8_t> address = {0x81, 0x20, 0x00};  // 2081h:00 (little endian index!)

    // Position = 0 (4 bytes)
    std::vector<uint8_t> value(4, 0x00);

    long ret = WriteSDO(address, value);

    if (ret != 0) {
        std::cerr << "[ERROR] ResetEncoder: SDO write returned " << ret << std::endl;
        return -1;
    }

    std::cout << "[INFO] Encoder reset via SDO (2081h written with 0)\n";
    return 0;
}

// ============================================================
// Configuration
// ============================================================

long  CiA402Device::SetEnc_res(int lines)
{
    encoder_resolution = lines;
    return 0;
}

long  CiA402Device::SetRed_Mot(float reduction_ratio)
{
    reduction_ratio_motor = reduction_ratio;
    return 0;
}

long  CiA402Device::SetSampling_period(float sampling_period)
{
    SampSL = sampling_period;
    return 0;
}

// ============================================================
// Conversion Helpers
// ============================================================

vector<uint8_t> data32to4x8(uint32_t in)
{

    vector<uint8_t> retvalue(4);
    retvalue[0] = in&0x000000FF;
    retvalue[1] = (in&0x0000FF00)>>8;
    retvalue[2] = (in&0x00FF0000)>>16;
    retvalue[3] = (in&0xFF000000)>>24;

    return retvalue;

}

vector<uint8_t> data16to2x8(uint16_t in)
{

    vector<uint8_t> retvalue(2);
    retvalue[0] = in&0x000000FF;
    retvalue[1] = (in&0x0000FF00)>>8;

    return retvalue;

}
