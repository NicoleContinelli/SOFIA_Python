#include "SerialArduino.h"

using namespace std;




SerialArduino::SerialArduino(string portName)
{
//    QApplication a(argc, argv);
//    QApplication a(0, 0);
//    QCoreApplication app();
        arduino_is_available = false;
        arduino_port_name = "";
        port = new QSerialPort;
        dataSize = 20;
        dataSensor.resize(dataSize);
        oriString.resize(dataSize);
        incliString.resize(dataSize);

        ///Port connection.
        // Options: QSerialPort::Baud<speed>
        // <speed> one of: 1200,2400,4800,9600,19200,38400,57600,115200
        qint32 baudrate =  QSerialPort::Baud19200;

        //Parte # 2,buscar puertos con los identificadores de Arduino
        qDebug() << "Number of available ports: " << QSerialPortInfo::availablePorts().length();
        foreach(const QSerialPortInfo &serialPortInfo, QSerialPortInfo::availablePorts()){
//            qDebug() << "Has vendor ID: " << serialPortInfo.hasVendorIdentifier();
            if(serialPortInfo.hasVendorIdentifier() && serialPortInfo.portName().toStdString()==portName)
            {
                qDebug() << "Port: " << serialPortInfo.portName();
                qDebug() << "Vendor ID: " << serialPortInfo.vendorIdentifier();
                qDebug() << "Has Product ID: " << serialPortInfo.hasProductIdentifier();
                qDebug() << "Product ID: " << serialPortInfo.productIdentifier();
                qDebug() <<"\n";

//             }
//        }





//        foreach(const QSerialPortInfo &serialPortInfo, QSerialPortInfo::availablePorts())
//        {
////            if(serialPortInfo.hasVendorIdentifier() && serialPortInfo.hasProductIdentifier())
//            {
               if(serialPortInfo.vendorIdentifier() == arduino_uno_vendor_id)
               {
                   cout << "arduino_uno_vendor_id: " << arduino_uno_vendor_id;
                 if(serialPortInfo.productIdentifier() == arduino_MEGA)
                 {
                     cout << ". Arduino_MEGA: " << arduino_MEGA;

                    arduino_port_name=serialPortInfo.portName();
                    cout << ". Arduino_port_name: " << arduino_port_name.toUtf8().constData() << endl;
                    port->setPortName(arduino_port_name);
                    arduino_is_available = port->open(QIODevice::ReadWrite);
                    if (arduino_is_available)
                    {
                        cout << "port->open" << endl;
                        break;
                    }

                 }
               }

               if(serialPortInfo.vendorIdentifier() == arduino_nano_vendor_id)
               {
                   cout << "arduino_uno_vendor_id: " << arduino_uno_vendor_id;
                 if(serialPortInfo.productIdentifier() == arduino_nano)
                 {
                     cout << ". Arduino_nano: " << arduino_nano;

                    arduino_port_name=serialPortInfo.portName();
                    cout << ". Arduino_port_name: " << arduino_port_name.toUtf8().constData() << endl;
                    port->setPortName(arduino_port_name);
                    arduino_is_available = port->open(QIODevice::ReadWrite);

                    if (arduino_is_available)
                    {
                        cout << "port->open" << endl;
                        break;
                    }
                 }
               }

            }
         }

//        if(arduino_is_available && arduino_port_name=="ttyACM0"){
            // open and configure the serialport

            if (arduino_is_available)
            {
                port->setDataTerminalReady(false); //from: https://forum.arduino.cc/index.php/topic,28167.0.html
                if (port->waitForReadyRead(10000))
                {

                    port->readLine(dataarray,dataSize);
                    dataSensor = string(dataarray);
                    cout << "Port initialization: "  << dec << dataSensor << endl;

                }
                else
                {
                    cout << "Port initialization: empty answer" << endl;
                }
            }
            else
            {
                arduino_is_available = false;
                cout << "port->error. Check if user is in dialout group (sudo usermod -a -G dialout <user>) and restart session." << endl;

            }

//            cout << "setBaudRate:" << port->setBaudRate(QSerialPort::Baud9600);
            cout << "setBaudRate:" << port->setBaudRate(baudrate);
            cout << "Baudrate: " << port->baudRate() << endl;
            cout << ", setDataBits: " << port->setDataBits(QSerialPort::Data8);
            cout << ", setParity: " << port->setParity(QSerialPort::NoParity);
            cout << ", setStopBits: " << port->setStopBits(QSerialPort::OneStop);
            cout << ", setFlowControl: " << port->setFlowControl(QSerialPort::NoFlowControl) << endl;
            //QObject::connect(arduino, SIGNAL(readyRead()), this, SLOT(readSerial()));
//    }


}


long SerialArduino::readSensor(double &incli, double &orien)
{

    long readResult;
//    //Ask for inclination value
    port->write("i",1);
//    //wait the data
    //This read should not block more than a second.
//    if(!port->waitForReadyRead(1000)) return -1;
    // waitForReadyRead(security factor * data string size * bits/byte * ms/s / port->baudRate())
    if (!port->waitForReadyRead(1.2*8*dataSize*1000/port->baudRate())) return -1;

    if( port->isReadable())
    {
        dataSensor = "";
//        cout << "Delete dataSensor -> " << dataSensor << endl;

        do
        {

            readResult = port->readLine(dataarray,dataSize);
//            cout << "Readresult :" << readResult <<  endl;
            dataSensor+= string(dataarray);

            if(readResult <= 0)
            {
                if (!port->waitForReadyRead(1.2*8*dataSize*1000/port->baudRate())) return -1;
//                cout << "Missed chars :" << readResult <<  endl;
            }

        }
        while(dataSensor[dataSensor.size()-1] != '\n' );

//        cout << "dataSensor -> " << dataSensor << endl;

//        for (int i=0;i<dataSize;i++)
//        {
//            //port->waitForReadyRead(1.2*8*1000/port->baudRate());
//            // waitForReadyRead(security factor * bits/byte * ms/s / port->baudRate())
//            if (!port->waitForReadyRead(1000*1.2*8*1000/port->baudRate()))
//            {
//                cout << "Port tiemout!!!" << endl;
//                cerr << "Port tiemout!!!" << endl;
//                return -1;
//            }

//            //Data read line
//            port->getChar(&dataSensor[i]);
//            if (dataSensor[i]== '\n') break;
//        }

        //Here the data string is separated in orientation and inclination values

        incliString=dataSensor;
        oriString=dataSensor;
        //Find ',' in data sensor to divide in incl and orient
        for (uint i=0;i<dataSensor.size();i++)
        {
            if (dataSensor[i]==',')
            {
                incliString=incliString.erase(i,dataSensor.size());
                oriString=oriString.erase(0,i+1);
            }
        }

        try
        {
            oriString=oriString.erase(0,1);
            orien = stod(oriString);
            incliString=incliString.erase(0,1);
            incli = stod(incliString);
        }
        catch (exception& e)
        {
          cout << "Standard exception: " << e.what() << endl;
          cout << "Sensor received -> icnli:" <<incliString << "; ori:" <<oriString << endl;
        }

//        //Identify data between incl and orient
//        if (incliString[0]== 'i' || oriString[0]== 'o')
//        {
//            if (incliString[1] < '0' || incliString[1] > '9')
//            {
//                cout << "Wrong incliString!!! ->" << dec << incliString[1] << endl;
//                cerr << "Wrong incliString!!! ->" << dec << incliString[1] << endl;
//                return -1;

//            }
//            else
//            {
//                //remove the initial letter (i/o)
//                incliString=incliString.erase(0,1);
//                incli = stof(incliString);
//            }
//            if (oriString[1] < '0' || oriString[1] > '9')
//            {
//                cout << "Wrong oriString: " << dec << oriString[1] << endl;
//                cerr << "Wrong oriString: " << dec << oriString[1] << endl;
//                return -1;

//            }
//            else
//            {
//                //remove the initial letter (i/o)
//                oriString=oriString.erase(0,1);
//                orien = stof(oriString);
//            }

//        }
//        else
//        {
//            return -1;
//        }


    }


    return 0;

}

long SerialArduino::estimateSensor(double &incli, double &orien)
{

    if (readSensor(incli,orien)<0)
    {
        //use estimation
        incli=incli1+(incli1-incli0);
        orien=orien1+(orien1-orien0);
        cout << "Cant read sensor: estimated value!!" << endl;
    }
    else
    {
        //use read values
        //and store new values
        incli0=incli1;
        orien0=orien1;
        incli1=incli;
        orien1=orien;
    }



    return 0;

}

bool SerialArduino::getArduino_is_available() const
{
    return arduino_is_available;
}
