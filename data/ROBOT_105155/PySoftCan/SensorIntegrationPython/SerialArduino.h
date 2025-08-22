#ifndef SERIALARDUINO_H
#define SERIALARDUINO_H

#include <iostream>
#include <string>

#include <QSerialPort>
#include <QSerialPortInfo>
#include <QDebug>
#include <QtCore>

using namespace std;

class SerialArduino
{
public:
    SerialArduino(string portName = "ttyACM0");

    long readSensor(double &incli, double &orien);
    long estimateSensor(double &incli, double &orien);



    bool getArduino_is_available() const;

private:
    QSerialPort *port;
    static const quint16 arduino_uno_vendor_id = 9025;
    static const quint16 arduino_nano_vendor_id = 1027;

    static const quint16 arduino_MEGA = 66;
    static const quint16 arduino_nano = 24577;

    QString arduino_port_name;
    bool arduino_is_available;
    QByteArray dataread;
    QByteArray datareadInc;
    QByteArray datareadOri;
    QString serialBuffer, data1, data2;
    string oriString, incliString;
    string dataSensor;
    char dataarray[20];
    long dataSize;

    int x;
    float theta, phi;

    //estimateSensor variables
    double incli0,incli1;
    double orien0,orien1;
};

#endif // SERIALARDUINO_H
