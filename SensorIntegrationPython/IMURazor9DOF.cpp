#include "IMURazor9DOF.h"

IMURazor9DOF::IMURazor9DOF(string portName) : SerialComm(portName)
{
    SetBaudRate(57600); //Default value
    for (int i=0;i<16;i++)
    {
        cout << GetLine() << endl;
    }

    att.setMagCalib(1.0, 0.0, 0.0); //Device 3DMGX10 has no magnetometer
    att.setGyroBias(bx,by,bz); //Setting of gyro bias

}

long IMURazor9DOF::GetPitchRollYaw(double dts, double &o_pitch, double &o_roll, double &o_yaw)
{
    line = GetLine();
    line.erase(1,1);
//    cout << line << endl;

    p0=1;
    stringstream sline(line);
    for (int i=0;i<9;i++)
    {
        try
        {
            getline(sline,tmp,',');
            gam[i] = stod(tmp);
//            cout << " tmp: " << tmp << endl;

        }
        catch (exception& e)
        {
          cout << "Standard exception: " << e.what() << endl;
          cout << "Sensor received -> icnli:" <<tmp << "; ori:" <<line << endl;
        }

        att.update(dts,gam[3]*M_PI/180,gam[4]*M_PI/180,gam[5]*M_PI/180,gam[0],gam[1],gam[2],gam[6],gam[7],gam[8]);
    //    pitch = estimador.eulerPitch();
    //    roll = estimador.eulerRoll();
        o_pitch = att.fusedPitch();
        o_roll = att.fusedRoll();
        o_yaw = att.fusedYaw();


    }
    return 0;
}

long IMURazor9DOF::GetYawPitchRoll(double dts, double &o_yaw, double &o_pitch, double &o_roll)
{
    line = GetLine();
//    line.erase(1,1);
//    cout << line << endl;

    p0=1;
    stringstream sline(line);
    for (int i=0;i<3;i++)
    {
        try
        {
            getline(sline,tmp,',');
            gam[i] = stod(tmp);
//            cout << " tmp: " << tmp << endl;

        }
        catch (exception& e)
        {
          cout << "Standard exception: " << e.what() << endl;
          cout << "Sensor received -> icnli:" <<tmp << "; ori:" <<line << endl;
        }


        o_pitch = gam[1];
        o_roll = gam[2];
        o_yaw = gam[0];


    }
    return 0;
}

