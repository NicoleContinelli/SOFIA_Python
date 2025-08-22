#include "SerialComm.h"

// -------------------------  Constructor  ----------------------------

SerialComm::SerialComm(string portName, long new_baudrate)
{
    port = new boost::asio::serial_port(io);
    port->open(portName);
    if (port->is_open())
    {
         cout << "Port " << portName << " has been correctly initialized" << endl;
         SetBaudRate(new_baudrate);

    }
    else
    {
         cout << "Port " << portName << " can't be opened" << endl;
    }
}

long SerialComm::SetBaudRate(ulong new_baudrate)
{
    port->set_option(boost::asio::serial_port_base::baud_rate(new_baudrate));

    return 0;
}

// --------------------------------------------------------------------

// -------------------------  Read functions  -------------------------

bool SerialComm::ReadLine()
{
    string reading;
    //We'll read data till standar final carriage \n
    boost::asio::read_until( *port, buffer, "\n", error );
    std::istream str(&buffer); //Transform our info buffer into a string
    std::getline(str, reading); //Copy of the info from our buffer to our new string
//    cout << "Read data: " << reading << endl;
    return true;
}

string SerialComm::GetLine()
{
    string reading;
    //We'll read data till standard final carriage \n
    boost::asio::read_until( *port, buffer, "\n", error );
    std::istream str(&buffer); //Transform our info buffer into a string
    std::getline(str, reading); //Copy of the info from our buffer to our new string
//    cout << "Read data: " << reading << endl;
    return reading;
}

bool SerialComm::ReadChar(){
    char a;
    //This function will read a single char
    boost::asio::read(*port,boost::asio::buffer(&a, 1));
//    cout << "Read char: " << a << ", en int es: "<< int(a)<< endl;
    return true;
}

char SerialComm::GetChar(){

    char a;
    //This function will read and get a single char
    boost::asio::read(*port,boost::asio::buffer(&a, 1));
//    cout << "Read char: " << a << ", en int es: "<< int(a)<< endl;
    return a;
}

//This function will read a given number of chars
string SerialComm::GetChars(int size)
{
    if (size > MAX_READ_CHARS)
    {
        cerr << "MAX_READ_CHARS. Use chunks of maximum: " << MAX_READ_CHARS  << endl;
        cout << "MAX_READ_CHARS. Use chunks of maximum: "  << MAX_READ_CHARS  << endl;
        boost::asio::read(*port,boost::asio::buffer(charbuff, MAX_READ_CHARS));
    }
    else
    {
        boost::asio::read(*port,boost::asio::buffer(charbuff,size*sizeof(char)) );
    }

//    charbuff[size]='\n';
//    string reading(charbuff);
    reading.resize(size);
    for (uint i=0; i<size;i++)
    {
        reading[i]=charbuff[i];
    }
//    cout << "GetChars " << size << " total vs read:" << reading.size() << endl;

//    cout << "El conjunto de los " << size << " charts leidos es: " << reading << endl;
    return reading;
}

string SerialComm::GetNumberofChars(int size){

    //This function will read a concrete number of chars
    char a;
    string reading;
    for (int i=0; i<= size-1;i++){
    boost::asio::read(*port,boost::asio::buffer(&a, 1));
    reading += a;
    }
//    cout << "El conjunto de los " << size << " charts leidos es: " << reading << endl;
    return reading;
}

///
/// \brief SerialComm::ReadAndFind
/// \param delim: string with delimiter
/// \param read_available(out): Reading of all available data to the moment
/// \return : Number of characters till the delimiter
///
long SerialComm::ReadAndFind(string delim, string & read_available){

//    cout <<" Read until:" << a[0] << endl;
//    read_available.clear();
    charsUntil = boost::asio::read_until(*port, boost::asio::dynamic_buffer(read_available), delim, error );
    charsRead = read_available.size();
//    std::istream str(&buffer); //Transform our info buffer into a string
//    std::getline(str, lineRead); //Copy of the info from our buffer to our new string
//    cout << "Read data: " << charsRead << endl;
//    cout << "Position " << charsUntil << " total vs read:" << charsRead << endl;


//    cout << "El conjunto de los " << size << " charts leidos es: " << reading << endl;
    return charsUntil;
//    return lineRead;
}

// ---------------------------------------------------------------------

// -------------------------  Write functions  -------------------------

long SerialComm::WriteLine(string in_str){

    //This function will write a specified data packet via serial comm
    //We want to be sure that the data packet we're sending to our device ends up with \n (standard protocol)

    int flagcomprobacion=0;
    string check;
    string a;
    string b;
    string finalcarriage = "\\n";

    for (unsigned int i=0 ; i<=in_str.size()-1;i++){

        //We read every single char of the send string
        //We need to find final carriage. If we find so, 'flagcomprobacion' is set to 1.
        //Final carriage is \n.

        if (i>0){
        b = in_str.at(i);
        a = in_str.at(i-1);
        check = a+b;
        }

        if (check == finalcarriage){
             flagcomprobacion=1;
         }
    }

    //If we don't, final carriage will be add at the end of the string to apply standard communication protocol.
    if (flagcomprobacion==0){
        in_str+='\n';
    }

    //Finally, we sent our string with final carriage added
     charsWritten = boost::asio::write(
                *port,
                boost::asio::buffer(in_str.c_str(), in_str.size()),
                boost::asio::transfer_at_least(in_str.size()),
                error
                );

     if(charsWritten<=0)
     {
         cout << "Not responding. No data" << endl;
         return -1;
     }

     return charsWritten;
}

// ---------------------------------------------------------------------

// -------------------------  Check functions  -------------------------

long SerialComm::CheckLine(string checkline, string writenline)
{

    writenline.resize(checkline.size());
    return writenline.compare(checkline);

}

/*bool SerialComm::CheckLine(string checkline, string writenline){

    //Implemented timer to avoid infinite loops. If sensor doesnt send back correct answer within a concrete time, the message is writen again
    std::clock_t start;

    string deviceanswerr;
    int flag1=0;
    int flag2=0;
    bool flag4=false;
    int flag3=0;
    char deviceanswer_desc;
    char deviceanswer_length;
    char a;


    //We use this func to read a line and to compare it with the one we want
    //If they match, func will return 1.

    do{
             start = std::clock();

        do{
            //Reset of some variables to avoid infinite loops
            deviceanswerr.clear();
            flag1=0;
            flag2=0;
            flag4=false;
            flag3=0;

            do{

            boost::asio::read(*port,boost::asio::buffer(&a, 1));
            switch (a) {
            case 'u':{
                flag1=1;
                deviceanswerr+=a;
                break;}
            case 'e':{
                if (flag1==1){
                    flag2=1;
                    deviceanswerr+=a;
                }else{
                    flag1=0;
                    deviceanswerr+=a;
                }
                break;}
            default:{
                deviceanswerr.clear();
                break;}
            }

        }while (flag2==0);

        boost::asio::read(*port,boost::asio::buffer(&deviceanswer_desc, 1));
        deviceanswerr +=deviceanswer_desc;
        boost::asio::read(*port,boost::asio::buffer(&deviceanswer_length, 1));
        deviceanswerr +=deviceanswer_length;

        if (int(deviceanswer_length) != int(checkline.at(4))){
            flag3=0;

            if (std::clock() - start >=50000){
                //To avoid infinite loops
                boost::asio::write(
                            *port,
                            boost::asio::buffer(writenline.c_str(), writenline.size()),
                            boost::asio::transfer_at_least(writenline.size()),
                            error
                            );
            }
        }else{
            flag3=1;
        }

        }while (flag3==0);

        for (int i=0; i<= ((int)deviceanswer_length+1); i++){
            boost::asio::read(*port,boost::asio::buffer(&a, 1));
            deviceanswerr +=a;
        }

        if (deviceanswerr==checkline){
            flag4=true;
//            cout << "La cadena es correcta" << endl;

        }else{
            deviceanswerr.clear();
            flag4=false;
//            cout << "La cadena no es correcta" << endl;

        }
    }while(flag4==0);
    return flag4;
}
*/
