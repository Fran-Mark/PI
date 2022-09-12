#include "client.h"

Client::Client(char *hostname, int port)
{
    /* socket: create the socket */
    socketFd = socket(AF_INET, SOCK_STREAM, 0);
    helpers::throwErrorIf(socketFd < 0, "ERROR opening socket");
    /* gethostbyname: get the server's DNS entry */
    server = gethostbyname(hostname);
    helpers::throwErrorIf(server == NULL, "ERROR, no such host");
    /* build the server's Internet address */
    bzero((char *) &serverAddress, sizeof(serverAddress));
    serverAddress.sin_family = AF_INET;
    bcopy((char *)server->h_addr, 
         (char *)&serverAddress.sin_addr.s_addr,
         server->h_length);
    serverAddress.sin_port = htons(port);

    int isConnected = connect(socketFd, (struct sockaddr *)&serverAddress, sizeof(serverAddress));
    helpers::throwErrorIf(isConnected < 0, "ERROR connecting");
}
Client::~Client()
{
    close(socketFd);
}

void Client::sendMessage(void *message, int nBytes)
{
    helpers::writeNBytes(socketFd, message, nBytes);
}

void Client::receiveData(int port)
{
    struct sockaddr_in streamingAddress;
    bzero((char *) &streamingAddress, sizeof(streamingAddress));
    streamingAddress.sin_family = AF_INET;
    streamingAddress.sin_port = htons(port);

    int streamingSocketFd = socket(AF_INET, SOCK_STREAM, 0);
    helpers::throwErrorIf(streamingSocketFd < 0, "ERROR opening streaming socket");

    helpers::throwErrorIf(server == NULL, "ERROR, no such host");    
    bcopy((char *)server->h_addr, 
         (char *)&streamingAddress.sin_addr.s_addr,
         server->h_length);
         
    int isConnected = connect(streamingSocketFd, (struct sockaddr *)&streamingAddress, sizeof(streamingAddress));
    helpers::throwErrorIf(isConnected < 0, "ERROR connecting");

    //receive filename from socket
    int filenameLength;
    helpers::readNBytes(streamingSocketFd, &filenameLength, sizeof(filenameLength));
    char filename[filenameLength];
    helpers::readNBytes(streamingSocketFd, filename, filenameLength);
    std::string dataFilename = "../captures/client_side/data_" + std::string(filename);

    int fd = open(dataFilename.c_str(), O_WRONLY | O_CREAT, 0666);

    helpers::throwErrorIf(fd < 0, "ERROR opening file");
    char line[SAMPLE_LINE_LENGTH];
    while(read(streamingSocketFd, line, SAMPLE_LINE_LENGTH) > 0){
        helpers::writeNBytes(fd, line, SAMPLE_LINE_LENGTH);
        bzero(line, SAMPLE_LINE_LENGTH);
    }
    close(fd);
    close(streamingSocketFd);
}

void Client::run()
{
   while (1){
        std::string stringBuffer;
        std::cout << "Ingrese los Two-element set parameters (TLEs)\n";
        std::cout << "Nombre:" << std::endl;
        std::getline(std::cin, stringBuffer);
        sendMessage((char*)stringBuffer.c_str(), TLE_LINE_LENGTH);
        std::cout << "Primera línea:" << std::endl;
        std::getline(std::cin, stringBuffer);
        sendMessage((char*)stringBuffer.c_str(), TLE_LINE_LENGTH);
        std::cout << "Segunda línea:" << std::endl;
        std::getline(std::cin, stringBuffer);
        sendMessage((char*)stringBuffer.c_str(), TLE_LINE_LENGTH);

        bool isValid;
        helpers::readNBytes(socketFd, &isValid, sizeof(isValid));
        if (isValid){
            std::cout << "TLE válido\n";
            std::cout << "Frecuencia [MHz]:" << std::endl;
            float freq;
            std::cin >> freq;
            sendMessage(&freq, sizeof(freq));
            break;
        }
        else{
            std::cout << "TLE inválido\n";
        }
    }

    uint8_t incomingDataFlag;
    helpers::readNBytes(socketFd, &incomingDataFlag, sizeof(incomingDataFlag));

    if (incomingDataFlag == 1){
        std::cout << "Iniciando captura de datos\n";
        uint16_t netPort;
        helpers::readNBytes(socketFd, &netPort, sizeof(netPort));
        uint16_t port = ntohs(netPort);
        std::cout << "Puerto: " << port << std::endl;
        receiveData(port);
        std::cout << "Finalizando captura de datos\n";
    }
    else{
        std::cout << "Error al iniciar captura de datos\n";
    }
}

