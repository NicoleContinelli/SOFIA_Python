#include "imu3dmgx510.h"

#include <iostream>
#include <ios>
#include <cmath>
#include <typeinfo>

// -------------------------  Constructor  -------------------------------

IMU3DMGX510::IMU3DMGX510(string portName, int new_freq) : port(portName)
{

    port.SetBaudRate(115200);

    //3DMGX10 device will be calibrated once port where it has been connected to has been correctly opened thanks to SerialComm constructor.
    estimador.setMagCalib(0.0, 0.0, 0.0); //Device 3DMGX10 has no magnetometer
    estimador.setGyroBias(bx,by,bz); //Setting of gyro bias

//    estimador.setPIGains(Kp, Ti, KpQuick, TiQuick); //Setting of device gains
//    estimador.setAccMethod(estimador.ME_FUSED_YAW);        // Optional: Use if you wish to experiment with varying acc-only resolution methods
//    set_reset();

//    //Calibration
    set_IDLEmode();

    Ping();

    set_freq(new_freq);
    set_devicetogetgyroacc();
    set_streamon();
    cout << "Calibrating IMU..." << endl;
    calibrate();

    //Once the device is correctly connected, it's set to IDLE mode to stop transmitting data till user requests it
    set_IDLEmode();

    double initPitch,initiRoll, initYaw;
    for (int i = 0; i < 200; ++i) {
//        GetPitchRoll(initPitch,initiRoll);
//        GetPitchRollYaw(initPitch,initiRoll,initYaw);//CR

    }

    cout << "Calibration done" << endl;

}

// -----------------------------------------------------------------------

// -------------------------  Initialization  ----------------------------

bool IMU3DMGX510::check() {
    bool check;
    port.WriteLine(idle);
    do{
    check = port.CheckLine(ok_idle,idle);
    }while (check==false);
    return check;
}

bool IMU3DMGX510::set_freq(int frequency){
    freq=frequency;
    period = 1 / freq;
    return true;
}

long IMU3DMGX510::calibrate(){

    //We will obtain initial offset to correct it the moment we make measures
    string answer, str, str1, str2, str3, str4, str5;
    string line;
    char c;
    char longitud;
    char descriptor;
    double roll=0.0;
    double pitch=0.0;
    double yaw=0.0; //CR

    ulf accx,accy,accz,gyrox,gyroy,gyroz;

    for (int h=0; h<=CAL_LOOPS;h++)
    {

        //Reset of the variables to avoid infinite loops.
        answer.clear();
        str.clear();
        str1.clear();
        str2.clear();
        str3.clear();
        str4.clear();
        str5.clear();
        int comp = 0;
        int fin = 0;
        double f=0;
        double f1=0;
        double f2=0;
        double f3=0;
        double f4=0;
        double f5=0;
        c = '0';
        longitud = '0';
        descriptor = '0';

        line = port.GetLine();

//        cout << line << endl;


        do{
            c = port.GetChar();
            switch (c) {
            case 'u':{
                comp=1;
                answer+=c;
                break;}
            case 'e':{
                if (comp==1){
                    fin=1;
                    answer+=c;
                }else{
                    comp=0;
                    answer+=c;
                }
                break;}

            default:{
                answer+=c;
                break;}

            }
        }while(fin==0);

        descriptor = port.GetChar();
        answer+=descriptor;

        longitud = port.GetChar();
        answer+=longitud;


        for (int j = 0 ; j<= ((int)longitud + 1) ; j++){
            c = port.GetChar();
            answer+=c;
        }

        if (int(longitud) == 28 && int(descriptor) == -128){
            str =hex(answer.substr(6,4));
            std::stringstream ss(str);
            ss >> std::hex >> accx.ul;
            f = accx.f;

            str1 =hex(answer.substr(10,4));
            std::stringstream ss1(str1);
            ss1 >> std::hex >> accy.ul;
            f1 = accy.f;

            str2 =hex(answer.substr(14,4));
            std::stringstream ss2(str2);
            ss2 >> std::hex >> accz.ul;
            f2 = accz.f;

            str3 =hex(answer.substr(20,4));
            std::stringstream ss3(str3);
            ss3 >> std::hex >> gyrox.ul;
            f3 = gyrox.f;

            str4 =hex(answer.substr(24,4));
            std::stringstream ss4(str4);
            ss4 >> std::hex >> gyroy.ul;
            f4 = gyroy.f;

            str5 =hex(answer.substr(28,4));
            std::stringstream ss5(str5);
            ss5>> std::hex >> gyroz.ul;
            f5 = gyroz.f;

            if (isnan(f3*f4*f5*f*f1*f2)) return -1;
            estimador.update(period,f3,f4,f5,f*9.81,f1*9.81,f2*9.81,0,0,0);
            //estimador.update(period,f3,f4,f5,f,f1,f2,0,0,0);//CR
            //stimador.update(period,0.01*(f3-0.5*f4),0.01*(f4-0.5*f3),0.01*f5,f,f1,f2,0,0,0);


            roll = estimador.eulerRoll();
            pitch= estimador.eulerPitch();
            yaw= estimador.eulerYaw();

            //First 150 measures are ignored because they are not stable
            if (h>=150 && h<=500){
                rolloffset= rolloffset+ roll ;
                pitchoffset= pitchoffset +pitch ;
                yawoffset= yawoffset +yaw;
            }
            true_yawoff=0;
        }
    }
//    rolloffset = rolloffset / 350;
//    pitchoffset = pitchoffset / 350;

////    rolloffset=rolloffset*180/M_PI;
////    pitchoffset=pitchoffset*180/M_PI;
//    cout << "Initial offsets: \n" << "Roll = " << rolloffset << "\n" << "Pitch = " << pitchoffset << endl;
    return 0;
}

// -----------------------------------------------------------------------

// -------------------------  Configuration  -----------------------------

long IMU3DMGX510::Ping()
{

    port.WriteLine(ping);
    usleep(T_WAIT);
//    ShowCode(port.GetChars(10));
    return ReadACK(ok_ping);

}

long IMU3DMGX510::set_IDLEmode()
{

    //We send data to set 3DMGX10 to IDLE mode


    //3DMGX10 will answer back a message showing if any error appeared in the process
    //We must read it
//    for (int t=0; t<T_OUT; t+=T_WAIT)
//    {
        port.WriteLine(idle);
        usleep(T_WAIT);
        return FindPortLine(ok_idle,portResponse);
//        ShowCode(portResponse);
//        return ReadACK(ok_idle);
//        GetPortLine(portResponse);

//        usleep(T_WAIT);
//        cout << port.GetLine();

//        if (ReadACK(ok_idle)==0) break;
//    }


//    do{
//    comprobacion = port.CheckLine(respuestacorrectaidle,idle);
//    }while (comprobacion==false);

//    return 0;
}

long IMU3DMGX510::set_streamon()
{
    //We activate data stream
    port.WriteLine(streamon);
    //3DMGX10 will answer back a message showing if any error appeared in the process
    //We must read it
    usleep(T_WAIT);
    return FindPortLine(ok_streamon,portResponse);

//    return ReadACK(ok_streamon);
//        comprobacion = port.CheckLine(ok_streamon,streamon);
//        if (comprobacion != 0){
//            cout << "set_streamon. Envio o respuesta incorrectos" << endl;
//        }
//    return comprobacion;
}

long IMU3DMGX510::set_streamoff(){
    //We deactivate data stream
    port.WriteLine(streamoff);
    //3DMGX10 will answer back a message showing if any error appeared in the process
    //We must read it
    usleep(T_WAIT);
    return FindPortLine(ok_streamon,portResponse);

//    return ReadACK(ok_streamon);

//    bool comprobacion = port.CheckLine(ok_streamon,streamoff);
//    if (comprobacion != 0){
//                    cout << "set_streamoff. Envio o respuesta incorrectos" << endl;
//    }
//    return comprobacion;
}

long IMU3DMGX510::set_reset(){
    //We reset IMU
//    port.WriteLine(reset);
    //3DMGX10 will answer back a message showing if any error appeared in the process
    //We must read it
    if (port.WriteLine(reset) == 0)
    {
        cout << "Not responding. No data" << endl;
        return -1;
    }

    for (int t=0; t<T_OUT; t+=T_WAIT)
    {

        usleep(T_WAIT);

        cout << "loop" << t << endl;
        if (ReadACK(ok_reset)==0) break;
    }
//    usleep(T_WAIT);
//    GetPortLine(portResponse);
//    ReadACK(ok_reset);
//    bool comprobacion = port.CheckLine(respuestacorrectareset,reset);
//    if (comprobacion != 0){
//                    cout << "set_reset. Envio o respuesta incorrectos" << endl;
//    }
    return 0;
}

long IMU3DMGX510::set_devicetogetgyroacc(){
    //We will prepare our device to get gyros and accs values
    //Freq will be introduced by user (1Hz or 100Hz atm)
    if(freq==1){
        port.WriteLine(gyracc1);
        comprobacion = port.CheckLine(setok,gyracc1);
    }else if (freq == 50){
        port.WriteLine(gyracc50);
        comprobacion = port.CheckLine(setok,gyracc50);
    }else if (freq == 100){
        port.WriteLine(gyracc100);
        comprobacion = port.CheckLine(setok,gyracc100);
    }else if (freq == 500){
        port.WriteLine(gyracc500);
        comprobacion = port.CheckLine(setok,gyracc500);
    }else if (freq == 1000){
        port.WriteLine(gyracc1000);
        comprobacion = port.CheckLine(setok,gyracc1000);
    }else{
        port.WriteLine(gyracc100);
        comprobacion = port.CheckLine(setok,gyracc100);
    }
    usleep(T_WAIT);

    return ReadACK(setok);

//    if (comprobacion != 0){

//        cout << "set_devicetogetgyroacc. Envio o respuesta incorrectos" << endl;
//        ShowCode(gyracc100);
//        ShowCode(setok);
//    }
//    return comprobacion;
}

long IMU3DMGX510::set_devicetogetgyro(){
    //We will prepare our device to get gyros and accs values
    //Freq will be introduced by user (1Hz or 100Hz atm)
    if (freq==1){
        port.WriteLine(imudata1);
        comprobacion = port.CheckLine(setok,imudata1);
    }else if (freq==100){
        port.WriteLine(imudata100);
        comprobacion = port.CheckLine(setok,imudata100);
    }else if (freq==1000){
        port.WriteLine(imudata1000);
        comprobacion = port.CheckLine(setok,imudata1000);
                    printf(">>>1000 \n");
    }else{
        port.WriteLine(imudata100);
        comprobacion = port.CheckLine(setok,imudata100);
    }

    if (comprobacion != 0){
        cout << "set_devicetogetgyro. Envio o respuesta incorrectos" << endl;
    }
    return comprobacion;
}


// -----------------------------------------------------------------------


// -------------------------  Getting data  ------------------------------

std::tuple <float, float, float> IMU3DMGX510::get_gyroPolling() {

    //We send data to set 3DMGX10 to polling mode
    port.WriteLine(polling);

    string reading;
    float gyroxvalue, gyroyvalue, gyrozvalue;

    //3DMGX10 will answer back a message with gyro values
    //We must read it
    reading = port.GetNumberofChars(20);

        //X
        ulf x;
        reading.substr(6,4);
        std::string str =hex(reading.substr(6,4));
        std::stringstream ss(str);
        ss >> std::hex >> x.ul;
        gyroxvalue = x.f;

        //Y
        ulf y;
        std::string str1 =hex(reading.substr(10,4));
        std::stringstream ss1(str1);
        ss1 >> std::hex >> y.ul;
        gyroyvalue = y.f;

        //Z
        ulf z;
        std::string str2 =hex(reading.substr(14,4));
        std::stringstream ss2(str2);
        ss2 >> std::hex >> z.ul;
        gyrozvalue = z.f;

    cout << "Our gyro velocities are: "<< gyroxvalue << " " << gyroyvalue << " " << gyrozvalue << endl;

    return std::make_tuple(gyroxvalue, gyroyvalue, gyrozvalue);
}


double* IMU3DMGX510::get_euleranglesPolling() {

    string reading;
    double roll, pitch, yaw;
    static double estimation[3];
    char c;
    int comp=0;
    int fin=0;

    //First time needs a mayor number of samples in order to get calibrated
    //After it, there is no need of taking such number of samples

    if (firsttime==0){

    for (int i =0; i<=100 ; i++){

        firsttime=1;

        //We send data to set 3DMGX10 to polling mode
        port.WriteLine(polling);

        //3DMGX10 will answer back a message with gyro and acc values
        //We must read it
        comp=0;
        fin=0;

        do{
            c = port.GetChar();
            switch (c) {
            case 'u':{
                comp=1;
                reading+=c;
                break;}
            case 'e':{
                if (comp==1){
                    fin=1;
                    reading+=c;
                }else{
                    comp=0;
                    reading+=c;
                }
                break;}

            default:{
                reading+=c;
                break;}

            }
        }while(fin==0);

        char descriptor = port.GetChar();
        reading+=descriptor;

        char longitud = port.GetChar();
        reading+=longitud;

        for (int j = 0 ; j<= ((int)longitud + 1) ; j++){
            c = port.GetChar();
            reading+=c;
        }

        if (int(longitud) == 28){
            ulf accx;
            std::string str =hex(reading.substr(6,4));
            std::stringstream ss(str);
            ss >> std::hex >> accx.ul;
            double f = accx.f;

            ulf accy;
            std::string str1 =hex(reading.substr(10,4));
            std::stringstream ss1(str1);
            ss1 >> std::hex >> accy.ul;
            double f1 = accy.f;

            ulf accz;
            std::string str2 =hex(reading.substr(14,4));
            std::stringstream ss2(str2);
            ss2 >> std::hex >> accz.ul;
            double f2 = accz.f;

            ulf gyrox;
            std::string str3 =hex(reading.substr(20,4));
            std::stringstream ss3(str3);
            ss3 >> std::hex >> gyrox.ul;
            double f3 = gyrox.f;

            ulf gyroy;
            std::string str4 =hex(reading.substr(24,4));
            std::stringstream ss4(str4);
            ss4 >> std::hex >> gyroy.ul;
            double f4 = gyroy.f;

            ulf gyroz;
            std::string str5 =hex(reading.substr(28,4));
            std::stringstream ss5(str5);
            ss5>> std::hex >> gyroz.ul;
            double f5 = gyroz.f;

            estimador.update(period,f3,f4,f5,f*9.81,f1*9.81,f2*9.81,0,0,0);
        }
    }
    }else{

        //We send data to set 3DMGX10 to polling mode
        port.WriteLine(polling);

        comp=0;
        fin=0;

        do{
            c = port.GetChar();
            switch (c) {
            case 'u':{
                comp=1;
                reading+=c;
                break;}
            case 'e':{
                if (comp==1){
                    fin=1;
                    reading+=c;
                }else{
                    comp=0;
                    reading+=c;
                }
                break;}

            default:{
                reading+=c;
                break;}

            }
        }while(fin==0);

        char descriptor = port.GetChar();
        reading+=descriptor;

        char longitud = port.GetChar();
        reading+=longitud;

        for (int j = 0 ; j<= ((int)longitud + 1) ; j++){
            c = port.GetChar();
            reading+=c;
        }

        if (int(longitud) == 28){
            ulf accx;
            std::string str =hex(reading.substr(6,4));
            std::stringstream ss(str);
            ss >> std::hex >> accx.ul;
            double f = accx.f;

            ulf accy;
            std::string str1 =hex(reading.substr(10,4));
            std::stringstream ss1(str1);
            ss1 >> std::hex >> accy.ul;
            double f1 = accy.f;

            ulf accz;
            std::string str2 =hex(reading.substr(14,4));
            std::stringstream ss2(str2);
            ss2 >> std::hex >> accz.ul;
            double f2 = accz.f;

            ulf gyrox;
            std::string str3 =hex(reading.substr(20,4));
            std::stringstream ss3(str3);
            ss3 >> std::hex >> gyrox.ul;
            double f3 = gyrox.f;

            ulf gyroy;
            std::string str4 =hex(reading.substr(24,4));
            std::stringstream ss4(str4);
            ss4 >> std::hex >> gyroy.ul;
            double f4 = gyroy.f;

            ulf gyroz;
            std::string str5 =hex(reading.substr(28,4));
            std::stringstream ss5(str5);
            ss5>> std::hex >> gyroz.ul;
            double f5 = gyroz.f;

            estimador.update(period,f3,f4,f5,f*9.81,f1*9.81,f2*9.81,0,0,0);
        }
     }

    estimation[0]=estimador.eulerRoll();
    estimation[1]=estimador.eulerPitch();
    estimation[2]=estimador.eulerYaw();
    return estimation;
}



long IMU3DMGX510::GetPitchRoll(double &pitch, double &roll)
{
//    GetPitchRollYaw(pitch,roll,tmpYaw);

    return 0;

}

double* IMU3DMGX510::GetPitchRollYaw(double &pitch, double &roll, double &yaw, double angles[])
{
    port.WriteLine(polling);
    portResponse.clear();

    //Really bad hardcoded time wait!!
    //TODO: Compute the wait time correctly!!
    usleep(10*1000); //10 milliseconds

    FindPortLine(poll_data,portResponse);
//    ShowCode(portResponse);

    string reading = portResponse;
    if (reading.size() < 32);
//        return -1;

    ulf accx;
    std::string str =hex(reading.substr(6,4));
    std::stringstream ss(str);
    ss >> std::hex >> accx.ul;
    double ax = accx.f;

    ulf accy;
    std::string str1 =hex(reading.substr(10,4));
    std::stringstream ss1(str1);
    ss1 >> std::hex >> accy.ul;
    double ay = accy.f;

    ulf accz;
    std::string str2 =hex(reading.substr(14,4));
    std::stringstream ss2(str2);
    ss2 >> std::hex >> accz.ul;
    double az = accz.f;

    ulf gyrox;
    std::string str3 =hex(reading.substr(20,4));
    std::stringstream ss3(str3);
    ss3 >> std::hex >> gyrox.ul;
    double gx = gyrox.f;

    ulf gyroy;
    std::string str4 =hex(reading.substr(24,4));
    std::stringstream ss4(str4);
    ss4 >> std::hex >> gyroy.ul;
    double gy = gyroy.f;

    ulf gyroz;
    std::string str5 =hex(reading.substr(28,4));
    std::stringstream ss5(str5);
    ss5>> std::hex >> gyroz.ul;
    double gz = gyroz.f;

    if (isnan(ax*ay*az*gx*gy*gz))
    {
        cout << ax*ay*az*gx*gy*gz << endl;
        estimador.setAttitudeFused(yaw,pitch, roll,1);
//        return -1;
    }

    {
        //accelerations x and y need -9.81???!!!!
//    estimador.update(period,0.01*(gx-0.5*gy),0.01*(gy-0.5*gx),0.01*gz,ax,ay,az,0,0,0);
    estimador.update(period,gx,gy,gz,ax,ay,az,0,0,0);
//    pitch = estimador.eulerPitch();
//    roll = estimador.eulerRoll();
    pitch = estimador.fusedPitch();
    roll = estimador.fusedRoll();
//    yaw = estimador.eulerYaw();
    //yaw = atan2(ay,ax); //PRUEBA CARLOS
    if (abs(gz)<0.003){
        gz=0;
    }
    true_yawoff=true_yawoff+(gz*period/2);
    yaw=true_yawoff;

    }
//    cout<< typeid(pitch).name() << '\n';
//    cout<< pitch << "," << roll << "," << roll << endl;
//    cout << "Values: "  << period << "," << gx << "," <<  gy<< "," << gz<< "," << ax<< "," << ay<< "," << az<< "," << endl;
    angles[0] = pitch;
    angles[1] = roll;
    angles[2] = yaw;
    return angles;

}


//GETPITCH >> FOR SENSOR IN PYTHON
double IMU3DMGX510::GetPitch(double pitch, double roll, double yaw)
{
    port.WriteLine(polling);
    portResponse.clear();

    //Really bad hardcoded time wait!!
    //TODO: Compute the wait time correctly!!
    usleep(10*1000); //10 milliseconds

    FindPortLine(poll_data,portResponse);
//    ShowCode(portResponse);

    string reading = portResponse;
    if (reading.size() < 32);
//        return -1;

    ulf accx;
    std::string str =hex(reading.substr(6,4));
    std::stringstream ss(str);
    ss >> std::hex >> accx.ul;
    double ax = accx.f;

    ulf accy;
    std::string str1 =hex(reading.substr(10,4));
    std::stringstream ss1(str1);
    ss1 >> std::hex >> accy.ul;
    double ay = accy.f;

    ulf accz;
    std::string str2 =hex(reading.substr(14,4));
    std::stringstream ss2(str2);
    ss2 >> std::hex >> accz.ul;
    double az = accz.f;

    ulf gyrox;
    std::string str3 =hex(reading.substr(20,4));
    std::stringstream ss3(str3);
    ss3 >> std::hex >> gyrox.ul;
    double gx = gyrox.f;

    ulf gyroy;
    std::string str4 =hex(reading.substr(24,4));
    std::stringstream ss4(str4);
    ss4 >> std::hex >> gyroy.ul;
    double gy = gyroy.f;

    ulf gyroz;
    std::string str5 =hex(reading.substr(28,4));
    std::stringstream ss5(str5);
    ss5>> std::hex >> gyroz.ul;
    double gz = gyroz.f;

    if (isnan(ax*ay*az*gx*gy*gz))
    {
        cout << ax*ay*az*gx*gy*gz << endl;
        estimador.setAttitudeFused(yaw,pitch, roll,1);
//        return -1;
    }

    {
        //accelerations x and y need -9.81???!!!!
//    estimador.update(period,0.01*(gx-0.5*gy),0.01*(gy-0.5*gx),0.01*gz,ax,ay,az,0,0,0);
    estimador.update(period,gx,gy,gz,ax,ay,az,0,0,0);
//    pitch = estimador.eulerPitch();
//    roll = estimador.eulerRoll();
    pitch = estimador.fusedPitch();
    roll = estimador.fusedRoll();
//    yaw = estimador.eulerYaw();
    //yaw = atan2(ay,ax); //PRUEBA CARLOS
    if (abs(gz)<0.003){
        gz=0;
    }
    true_yawoff=true_yawoff+(gz*period/2);
    yaw=true_yawoff;

    }
//    cout<< typeid(pitch).name() << '\n';
//    cout<< pitch << "," << roll << "," << roll << endl;
//    cout << "Values: "  << period << "," << gx << "," <<  gy<< "," << gz<< "," << ax<< "," << ay<< "," << az<< "," << endl;

    return pitch;

}



//GETROLL >> FOR SENSOR IN PYTHON
double IMU3DMGX510::GetRoll(double pitch, double roll, double yaw)
{
    port.WriteLine(polling);
    portResponse.clear();

    //Really bad hardcoded time wait!!
    //TODO: Compute the wait time correctly!!
    usleep(10*1000); //10 milliseconds

    FindPortLine(poll_data,portResponse);
//    ShowCode(portResponse);

    string reading = portResponse;
    if (reading.size() < 32);
//        return -1;

    ulf accx;
    std::string str =hex(reading.substr(6,4));
    std::stringstream ss(str);
    ss >> std::hex >> accx.ul;
    double ax = accx.f;

    ulf accy;
    std::string str1 =hex(reading.substr(10,4));
    std::stringstream ss1(str1);
    ss1 >> std::hex >> accy.ul;
    double ay = accy.f;

    ulf accz;
    std::string str2 =hex(reading.substr(14,4));
    std::stringstream ss2(str2);
    ss2 >> std::hex >> accz.ul;
    double az = accz.f;

    ulf gyrox;
    std::string str3 =hex(reading.substr(20,4));
    std::stringstream ss3(str3);
    ss3 >> std::hex >> gyrox.ul;
    double gx = gyrox.f;

    ulf gyroy;
    std::string str4 =hex(reading.substr(24,4));
    std::stringstream ss4(str4);
    ss4 >> std::hex >> gyroy.ul;
    double gy = gyroy.f;

    ulf gyroz;
    std::string str5 =hex(reading.substr(28,4));
    std::stringstream ss5(str5);
    ss5>> std::hex >> gyroz.ul;
    double gz = gyroz.f;

    if (isnan(ax*ay*az*gx*gy*gz))
    {
        cout << ax*ay*az*gx*gy*gz << endl;
        estimador.setAttitudeFused(yaw,pitch, roll,1);
//        return -1;
    }

    {
        //accelerations x and y need -9.81???!!!!
//    estimador.update(period,0.01*(gx-0.5*gy),0.01*(gy-0.5*gx),0.01*gz,ax,ay,az,0,0,0);
    estimador.update(period,gx,gy,gz,ax,ay,az,0,0,0);
//    pitch = estimador.eulerPitch();
//    roll = estimador.eulerRoll();
    pitch = estimador.fusedPitch();
    roll = estimador.fusedRoll();
//    yaw = estimador.eulerYaw();
    //yaw = atan2(ay,ax); //PRUEBA CARLOS
    if (abs(gz)<0.003){
        gz=0;
    }
    true_yawoff=true_yawoff+(gz*period/2);
    yaw=true_yawoff;

    }
//    cout<< typeid(pitch).name() << '\n';
//    cout<< pitch << "," << roll << "," << roll << endl;
//    cout << "Values: "  << period << "," << gx << "," <<  gy<< "," << gz<< "," << ax<< "," << ay<< "," << az<< "," << endl;

    return roll;

}



//GETYAW >> FOR SENSOR IN PYTHON
double IMU3DMGX510::GetYaw(double pitch, double roll, double yaw)
{
    port.WriteLine(polling);
    portResponse.clear();

    //Really bad hardcoded time wait!!
    //TODO: Compute the wait time correctly!!
    usleep(10*1000); //10 milliseconds

    FindPortLine(poll_data,portResponse);
//    ShowCode(portResponse);

    string reading = portResponse;
    if (reading.size() < 32);
//        return -1;

    ulf accx;
    std::string str =hex(reading.substr(6,4));
    std::stringstream ss(str);
    ss >> std::hex >> accx.ul;
    double ax = accx.f;

    ulf accy;
    std::string str1 =hex(reading.substr(10,4));
    std::stringstream ss1(str1);
    ss1 >> std::hex >> accy.ul;
    double ay = accy.f;

    ulf accz;
    std::string str2 =hex(reading.substr(14,4));
    std::stringstream ss2(str2);
    ss2 >> std::hex >> accz.ul;
    double az = accz.f;

    ulf gyrox;
    std::string str3 =hex(reading.substr(20,4));
    std::stringstream ss3(str3);
    ss3 >> std::hex >> gyrox.ul;
    double gx = gyrox.f;

    ulf gyroy;
    std::string str4 =hex(reading.substr(24,4));
    std::stringstream ss4(str4);
    ss4 >> std::hex >> gyroy.ul;
    double gy = gyroy.f;

    ulf gyroz;
    std::string str5 =hex(reading.substr(28,4));
    std::stringstream ss5(str5);
    ss5>> std::hex >> gyroz.ul;
    double gz = gyroz.f;

    if (isnan(ax*ay*az*gx*gy*gz))
    {
        cout << ax*ay*az*gx*gy*gz << endl;
        estimador.setAttitudeFused(yaw,pitch, roll,1);
//        return -1;
    }

    {
        //accelerations x and y need -9.81???!!!!
//    estimador.update(period,0.01*(gx-0.5*gy),0.01*(gy-0.5*gx),0.01*gz,ax,ay,az,0,0,0);
    estimador.update(period,gx,gy,gz,ax,ay,az,0,0,0);
//    pitch = estimador.eulerPitch();
//    roll = estimador.eulerRoll();
    pitch = estimador.fusedPitch();
    roll = estimador.fusedRoll();
//    yaw = estimador.eulerYaw();
    //yaw = atan2(ay,ax); //PRUEBA CARLOS
    if (abs(gz)<0.003){
        gz=0;
    }
    true_yawoff=true_yawoff+(gz*period/2);
    yaw=true_yawoff;

    }
//    cout<< typeid(pitch).name() << '\n';
//    cout<< pitch << "," << roll << "," << roll << endl;
//    cout << "Values: "  << period << "," << gx << "," <<  gy<< "," << gz<< "," << ax<< "," << ay<< "," << az<< "," << endl;

    return yaw;

}


long IMU3DMGX510::Reset()
{
    estimador.setAttitude(1,0,0,0);
    true_yawoff=0;

    return 0;

}

std::tuple <double*,double*,double*> IMU3DMGX510::get_gyroStreaming(int samples){

    //Decl. of the variables
     char c;
     string answer;
     char descriptor;
     char longitud;
     static double gyroxvector[10000];
     static double gyroyvector[10000];
     static double gyrozvector[10000];

     //The methodology will be the next:
     //   1) First, we will go through the 1st do-while loop untill we find 'ue' in our data packet. Then, varible "fin" will be set to 1.
     //   2) After reading 'ue', two next bites in the data packet are the descriptor and the lenght. Both will be read.
     //   3) We read the entire data packet with a for loop and its limit set by the lenght of the packet.
     //   4) We extract gyro values (gyrx,gyry,gyrz) from the recent read data packet.
     //   5) Repeat all steps "muestras" times.

     for (int h=0; h<=samples;h++){

         //Reset of some variables to avoid infinite loops
         int comp=0;
         int fin=0;

         do{
             c = port.GetChar();
             switch (c) {
             case 'u':{
                 comp=1;
                 answer+=c;
                 break;}
             case 'e':{
                 if (comp==1){
                     fin=1;
                     answer+=c;
                 }else{
                     comp=0;
                     answer+=c;
                 }
                 break;}

             default:{
                 break;}
             }
         }while(fin==0);

         descriptor = port.GetChar();
         answer+=descriptor;

         longitud = port.GetChar();
         answer+=longitud;

         for (int j = 0 ; j<= ((int)longitud + 1) ; j++){
             c = port.GetChar();
             answer+=c;
         }

         if (int(longitud) == 14){ //It must be 14
             //X

             ulf x;
             std::string str =hex(answer.substr(6,4));
             std::stringstream ss(str);
             ss >> std::hex >> x.ul;
             float f = x.f;
             gyroxvector[h] = f;

             //y

             ulf y;
             std::string str1 =hex(answer.substr(10,4));
             std::stringstream ss1(str1);
             ss1 >> std::hex >> y.ul;
             float f1 = y.f;
             gyroyvector[h] = f;

             //z

             ulf z;
             std::string str2 =hex(answer.substr(14,4));
             std::stringstream ss2(str2);
             ss2 >> std::hex >> z.ul;
             float f2 = z.f;
             gyrozvector[h] = f;
             }

         answer.clear();

         }

     return std::make_tuple(gyroxvector, gyroyvector, gyrozvector);
}
std::tuple <double*,double*,double,double> IMU3DMGX510::get_euleranglesStreaming(int samples){

    //Decl. of the variables
    string answer;
    char c;
    char longitud;
    char descriptor;
    static double rollvector[10000];
    static double pitchvector[10000];
    static double yawvector[10000];

    double rollaverage=0.0;
    double pitchaverage=0.0;
    double yawaverage=0.0;


    //        The methodology will be the next:
    //           1) First, we will go through the 1st do-while loop untill we find 'ue' in our data packet. Then, varible "fin" will be set to 1.
    //           2) After reading 'ue', two next bites in the data packet are the descriptor and the lenght. Both will be read.
    //           3) We read the entire data packet with a for loop and its limit set by the lenght of the packet.
    //           4) We extract float gyro values (gyrox,gyroy,gyroz) and float acc values(accx,accy,accz) from the recent read data packet.
    //           5) Now, we need to converts these values to Euler Angles(Pitch,Roll). "Attitude_estimator" lib is used to perform it.
    //           6) Once the receiving values are stable, we use the comment library to get Pitch,Roll. (If device is placed face down, values are stable since the very beginning).
    //           7) To correct the initial offset, we will get the average value of the first 125 values. This way, if our initial offset Yaw it 2'5, a correct value to the measurings of this angle will be: measuring - 2'5.
    //           8) Repeat all steps "muestras" times.

    for (int h=0; h<=samples;h++){

        //Reset of the variables to avoid infinite loops.
        answer.clear();
        int comp=0;
        int fin=0;

        do{
            c = port.GetChar();
            switch (c) {
            case 'u':{
                comp=1;
                answer+=c;
                break;}
            case 'e':{
                if (comp==1){
                    fin=1;
                    answer+=c;
                }else{
                    comp=0;
                    answer+=c;
                }
                break;}

            default:{
                answer+=c;
                break;}

            }
        }while(fin==0);

        descriptor = port.GetChar();
        answer+=descriptor;

        longitud = port.GetChar();
        answer+=longitud;

        for (int j = 0 ; j<= ((int)longitud + 1) ; j++){
            c = port.GetChar();
            answer+=c;
        }

        if (int(longitud) == 28){
            ulf accx;
            std::string str =hex(answer.substr(6,4));
            std::stringstream ss(str);
            ss >> std::hex >> accx.ul;
            double f = accx.f;

            ulf accy;
            std::string str1 =hex(answer.substr(10,4));
            std::stringstream ss1(str1);
            ss1 >> std::hex >> accy.ul;
            double f1 = accy.f;

            ulf accz;
            std::string str2 =hex(answer.substr(14,4));
            std::stringstream ss2(str2);
            ss2 >> std::hex >> accz.ul;
            double f2 = accz.f;

            ulf gyrox;
            std::string str3 =hex(answer.substr(20,4));
            std::stringstream ss3(str3);
            ss3 >> std::hex >> gyrox.ul;
            double f3 = gyrox.f;

            ulf gyroy;
            std::string str4 =hex(answer.substr(24,4));
            std::stringstream ss4(str4);
            ss4 >> std::hex >> gyroy.ul;
            double f4 = gyroy.f;

            ulf gyroz;
            std::string str5 =hex(answer.substr(28,4));
            std::stringstream ss5(str5);
            ss5>> std::hex >> gyroz.ul;
            double f5 = gyroz.f;

            //If sensor is placed face down, we can skip the if loop.
            if (h>=100 && h<=samples){

                estimador.update(period,f3,f4,f5,f*9.81,f1*9.81,f2*9.81,0,0,0);
                rollvector[h-100]=estimador.eulerRoll();
                pitchvector[h-100]=estimador.eulerPitch();
                yawvector[h-100]=estimador.eulerYaw();
                cout << "My attitude is : (" << estimador.eulerPitch() << "," << estimador.eulerRoll() << "," << estimador.eulerYaw() << ")" << endl;

                if(h>=225 && h<=350){

                    rollaverage= rollaverage + estimador.eulerRoll();
                    pitchaverage= pitchaverage + estimador.eulerPitch();
                    yawaverage= yawaverage + estimador.eulerYaw();


                    if (h==350){

                        rollaverage = rollaverage/125;
                        pitchaverage = pitchaverage/125;
                        yawaverage = yawaverage/125;
                    }
                }
            }
        }
    }

    return std::make_tuple(rollvector,pitchvector, rollaverage, pitchaverage);
}

double* IMU3DMGX510::EulerAngles() {

    static double EulerAngles[3];



//        if (abs(gy)<0.003){
//            gy=0;
//        }
//        if (abs(gx)<0.003){
//            gx=0;
//        }




    //////////////////////////////////////////

    port.WriteLine(polling);
    portResponse.clear();

    //Really bad hardcoded time wait!!
    //TODO: Compute the wait time correctly!!
    usleep(10*1000); //10 milliseconds

    FindPortLine(poll_data,portResponse);
//    ShowCode(portResponse);

    string reading = portResponse;
    if (reading.size() < 32){


        EulerAngles[2]=0/0;
        return EulerAngles;
    }

    ulf accx;
    std::string str =hex(reading.substr(6,4));
    std::stringstream ss(str);
    ss >> std::hex >> accx.ul;
    double ax = accx.f;

    ulf accy;
    std::string str1 =hex(reading.substr(10,4));
    std::stringstream ss1(str1);
    ss1 >> std::hex >> accy.ul;
    double ay = accy.f;

    ulf accz;
    std::string str2 =hex(reading.substr(14,4));
    std::stringstream ss2(str2);
    ss2 >> std::hex >> accz.ul;
    double az = accz.f;

    ulf gyrox;
    std::string str3 =hex(reading.substr(20,4));
    std::stringstream ss3(str3);
    ss3 >> std::hex >> gyrox.ul;
    double gx = gyrox.f;

    ulf gyroy;
    std::string str4 =hex(reading.substr(24,4));
    std::stringstream ss4(str4);
    ss4 >> std::hex >> gyroy.ul;
    double gy = gyroy.f;

    ulf gyroz;
    std::string str5 =hex(reading.substr(28,4));
    std::stringstream ss5(str5);
    ss5>> std::hex >> gyroz.ul;
    double gz = gyroz.f;

    if (isnan(ax*ay*az*gx*gy*gz))
    {
        cout << ax*ay*az*gx*gy*gz << endl;
        EulerAngles[0]=0/0; //rads
        EulerAngles[1]=0/0; //rads
        EulerAngles[2]=0/0;
        return EulerAngles;

    }

    {
    estimador.update(period,gx,gy,gz,ax*-9.81,ay*-9.81,az*-9.81,0,0,0);
    //estimador.update(period,gx,gy,gz,ax,ay,az,0,0,0);

    //estimador.update(period,0.01*(gx-0.5*gy),0.01*(gy-0.5*gx),0.01*gz,ax,ay,az,0,0,0);
    //estimador.update(period,gx,(gy),(gz),ax,ay,az,0,0,0);

    EulerAngles[0]=estimador.eulerRoll(); //rads
    EulerAngles[1]=estimador.eulerPitch(); //rads

    if (abs(gz)<0.003){
        gz=0;
    }

    EulerAngles[2]=true_yawoff+(gz*period/2);
    true_yawoff=true_yawoff+(gz*period/2);

    //EulerAngles[2]=estimador.eulerYaw();//-0.00078; //rads

    //cout <<true_yawoff<<" " <<EulerAngles[2]<<" "<<gz<<endl;

    EulerAngles[0] = EulerAngles[0]*180/M_PI; //rad to degrees
    EulerAngles[1] = EulerAngles[1]*180/M_PI; //rad to degrees
    EulerAngles[2] = EulerAngles[2]*180/M_PI; //rad to degrees

    }

    return EulerAngles;

}
double* IMU3DMGX510::GyroData(){

    //Decl. of the variables
    char c;
    string answer;
    char descriptor;
    char longitud;
    static double GyrosData[3];

    //Reset of the variables to avoid infinite loops.
    answer.clear();
    int comp=0;
    int fin=0;

    do{
        c = port.GetChar();
        switch (c) {
        case 'u':{
            comp=1;
            answer+=c;
            break;}
        case 'e':{
            if (comp==1){
                fin=1;
                answer+=c;
            }else{
                comp=0;
                answer+=c;
            }
            break;}

        default:{
            break;}
        }
    }while(fin==0);

    descriptor = port.GetChar();
    answer+=descriptor;

    longitud = port.GetChar();
    answer+=longitud;

    for (int j = 0 ; j<= ((int)longitud + 1) ; j++){
        c = port.GetChar();
        answer+=c;
    }

    if (int(longitud) == 14){ //It must be 14
        //X
        ulf x;
        std::string str =hex(answer.substr(6,4));
        std::stringstream ss(str);
        ss >> std::hex >> x.ul;
        float f = x.f;
        GyrosData[0] = f;

        //y
        ulf y;
        std::string str1 =hex(answer.substr(10,4));
        std::stringstream ss1(str1);
        ss1 >> std::hex >> y.ul;
        float f1 = y.f;
        GyrosData[1] = f1;

        //z
        ulf z;
        std::string str2 =hex(answer.substr(14,4));
        std::stringstream ss2(str2);
        ss2 >> std::hex >> z.ul;
        float f2 = z.f;
        GyrosData[2] = f2;
    }

    return GyrosData;
}

long IMU3DMGX510::ReadACK(string expected)
{

    portResponse.clear();

    //        portResponse = port.ReadUntil('u');

    GetPortLine(portResponse);
    //Checksums TODO: error handlng using checksums
    //Checksums are allways the last two bytes
    //        portResponse.pop_back();
    //        portResponse.pop_back();

    if (portResponse.compare(expected)!=0)
    {
        cout << "Retry, Waiting for: ";
        ShowCode(expected);
//        cout << "Not found, instead: ";
//        ShowCode(portResponse);

        cout << endl;

        return -1;

    }

    //        cout << "Found: " << endl;
    //        ShowCode(portResponse);

    return 0;
}



long IMU3DMGX510::GetPortLine(string & portLine)
{
//    cout << "GetPortLine Start " << endl;


    ulong readLineSize=0, delimiterPos = 0;
//    char check;

    delimiterPos = port.ReadAndFind("ue", portLine);

//    ShowCode(portLine);

//    The size of a comm line is formed by 4 header, payload, and 2 checksum bytes
    readLineSize = 4 + (uint)portLine[delimiterPos+2] + 2;
    portLine = portLine.substr(delimiterPos-2,readLineSize);

//    portLine = "ue";
//    portLine += port.GetChars(2);

//    descriptor = (uint)portLine[2];
//    payload = (uint)portLine[3];

//    cout << "Payload: " << (uint)payload << endl;

//    portLine = string("ue");
//    portLine += descriptor;
//    portLine += payload;
//    ShowCode(portLine);

//    portLine += port.GetChars(payload);

//    ShowCode(portLine);
//    cout << "GetPortLine End " << endl;

    return readLineSize;
}

///
/// \brief IMU3DMGX510::FindPortLine: Find a specific string in a port.
/// This function bloks until the string is read!!!
/// \param findText: The string to find.
/// \param wholeLine: The whole port line read.
/// \return
///
long IMU3DMGX510::FindPortLine(string findText, string &wholeLine)
{

    ulong readLineSize=0, delimiterPos = 0, initPos = 0;
    ulong delimSize=findText.size();

    delimiterPos = port.ReadAndFind(findText, wholeLine);
//    cout << "delimiterPos  " << delimiterPos << endl;

    initPos = delimiterPos - delimSize;

    readLineSize = delimiterPos + (uint)wholeLine[initPos +3] + 2;
//    cout << "initPos  " << initPos << endl;
//    printf("wholeLine[initPos +3] :%02hhx\n",wholeLine[initPos +3]);
//    cout << "readLineSize  " << readLineSize << endl;

//    ShowCode(wholeLine);

//    The size of a comm line is formed by delimiter, payload, and 2 checksum bytes
//    readLineSize = 4 + (uint)wholeLine[delimiterPos+2] + 2;
    wholeLine = wholeLine.substr(initPos,readLineSize);

    //TODO: Do timeout and return error when no string found!!
//    if (delimiterPos == wholeLine.size()) return -1;
    return 0;
}

long IMU3DMGX510::ShowCode(string showString)
{
    cout << "chars(" << showString.size() <<  ") :";
    for(uint i=0;i<showString.size();i++)
    {
        printf("%02hhx,",showString[i]);
//            cout << int(showString[i]) << ",";
    }
    cout << endl;

    return 0;

}


// -----------------------------------------------------------------------

