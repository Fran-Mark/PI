#include "server.h"


#define PAGE_SIZE 4096

//****Begin Server Class****//
Server::Server(int portNo_){
        portNo = portNo_;
        setUpSocket();
        cleanerThread = std::thread(&Server::cleanClients, this);
        _isRunning = true;
        std::cout << "Server: ready\n";
}   
Server::~Server(){
        close(socketFd);
        cleanerThread.join();
        killAllClients();
        mainThread.join();
        std::cout << "Server: closed\n";
}

void Server::start(){
    mainThread = std::thread(&Server::registerNewClients, this);  
}

void Server::stop(){
        _isRunning = false;
        cv.notify_one();
}

void Server::setUpSocket(){
        bzero((char *) &serverAddress, sizeof(serverAddress));
        serverAddress.sin_family = AF_INET;
        serverAddress.sin_addr.s_addr = INADDR_ANY;
        serverAddress.sin_port = htons(portNo);
        socketFd = socket(AF_INET, SOCK_STREAM, 0);
        helpers::throwErrorIf(socketFd < 0, "Error:: Socket opening failed");

        int value = 1;
        setsockopt(socketFd, SOL_SOCKET, SO_REUSEADDR, &value, sizeof(value));

        int isBound;
        isBound = bind(socketFd, (struct sockaddr *) &serverAddress, sizeof(serverAddress));
        helpers::throwErrorIf(isBound < 0, "Error:: Binding failed");

        listen(socketFd, 5);
        std::cout << "Server: listening...\n";
    }


int Server::getSocketFd(){
    return socketFd;
}

void Server::registerNewClients(){
    while(_isRunning){
        sockaddr_in clientAddress;
        socklen_t clientAddressLen = sizeof(clientAddress);
        fd_set fdSet;
        FD_ZERO(&fdSet);
        FD_SET(socketFd, &fdSet);
        timeval timeout;
        timeout.tv_sec = 2;
        timeout.tv_usec = 0;
        int isReady = select(socketFd + 1, &fdSet, NULL, NULL, &timeout);
        helpers::throwErrorIf(isReady == -1, "Error:: Select failed");
        if(isReady == 1){
            int clientSocketFd = accept(socketFd, (struct sockaddr *) &clientAddress, &clientAddressLen);
            helpers::throwErrorIf(clientSocketFd < 0, "Error:: Accept failed");
            std::cout << "Server: new client connected\n";
            clients.insert(new Client(clientSocketFd, this, &Server::handleClient));
        }
    }
}

void Server::cleanClients(){
    while (_isRunning){
        std::unique_lock<std::mutex> lk(mutex);
        cv.wait(lk);
        while (!clientsToKill.empty()){
            Client* client = clientsToKill.front();
            clientsToKill.pop();
            clients.erase(client);
            delete client;
        }
    }
}

void Server::killAllClients(){
    while (!clients.empty()){
        Client* client = *clients.begin();
        clients.erase(client);
        delete client;
    }
}

void Server::addClientToKill(Client* client){
    std::unique_lock<std::mutex> lck{mutex};
    clientsToKill.push(client);
    cv.notify_one();
}

bool Server::isRunning(){
    return _isRunning;
}

//****End Server Class****//

//****Begin Client Class****//
Server::Client::Client(int fd, Server* server_, void handler (Client* client)) {
        server = server_;
        socketFd = fd;
        th = std::thread(handler, this);
    }

Server::Client::~Client(){
        th.join();
        close(socketFd);
        std::cout << "Client destruido con éxito\n";
    }

void Server::Client::requestToDie(){  
    server->addClientToKill(this);
}

int Server::Client::getSocketFd(){
    return socketFd;
}

void Server::Client::setFilename(std::string filename_){
            filename = filename_;
            filenameWithPath = "../captures/server_side/" + filename_;
}

TLE Server::Client::readTLE(){

    char name[TLE_LINE_LENGTH];
    helpers::readNBytes(socketFd, name, TLE_LINE_LENGTH);

    char firstLine[TLE_LINE_LENGTH];
    helpers::readNBytes(socketFd, firstLine, TLE_LINE_LENGTH);
    
    char secondLine[TLE_LINE_LENGTH];
    helpers::readNBytes(socketFd, secondLine, TLE_LINE_LENGTH);

    std::cout<<"Nombre: "<<name<<"\nPrimera línea: "<<firstLine<<"\nSegunda línea: "<<secondLine<<"\n";

    return TLE(name, firstLine, secondLine); 
}

float Server::Client::readFreq(){
    float freq;
    helpers::readNBytes(socketFd, &freq, sizeof(freq));
    return freq*1000000;
}

void Server::Client::captureData(float freq, TLE tle, AccessController* accessController){
    //with the freq input determine the channel
    //with the tle determine de beamforming angles

    //call GNU Radio to capture the data and save it to a file
    std::cout << "Client: capturing\n";
    accessController->startWriting();
    BFmain(filenameWithPath.c_str());
    accessController->stopWriting();
    std::cout << "Client: capture completed\n";
    return;
}

void Server::Client::streamProcessedData(AccessController* accessController){
    in_port_t port = 0;
    struct sockaddr_in addr;
    bzero((char *) &addr, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(port);
    int streamingSocketFd = socket(AF_INET, SOCK_STREAM, 0);
    helpers::throwErrorIf(streamingSocketFd < 0, "ERROR opening socket");
    int enable = 1;
    if(setsockopt(streamingSocketFd, SOL_SOCKET, SO_REUSEADDR, &enable, sizeof(int)) < 0){
        helpers::throwErrorIf(true, "ERROR on setsockopt");
    }
    int bindStatus = bind(streamingSocketFd, (struct sockaddr *) &addr, sizeof(addr));
    helpers::throwErrorIf(bindStatus < 0, "ERROR on binding");
    //get sock addr port
    socklen_t addrLen = sizeof(addr);
    getsockname(streamingSocketFd, (struct sockaddr *) &addr, &addrLen);
    
    listen(streamingSocketFd,5);
    
    port = addr.sin_port;
    std::cout << "Client: streaming socket opened on port " << ntohs(port) << "\n";
    //send port to client
    helpers::writeNBytes(socketFd, &port, sizeof(port));

    socklen_t length = sizeof(addr);
    int streamingConnectionFd = accept(streamingSocketFd, (sockaddr *) &addr, &length);

    //send filename
    int filenameLen = filename.length();
    helpers::writeNBytes(streamingConnectionFd, &filenameLen, sizeof(filenameLen));
    helpers::writeNBytes(streamingConnectionFd, (void*)filename.c_str(), filenameLen);

    //open
    accessController->startReading();
    int fd = open(filenameWithPath.c_str(), O_RDONLY);
    helpers::throwErrorIf(fd < 0, "ERROR opening file");
    accessController->setFd(fd);

    int bytesRead = 0;

    int j = 0;
    while(1){ 
        int bytesToRead = accessController->getBytesToRead();
        if (bytesToRead == 0){
            break;
        }

        SampleLine* data = (SampleLine*) mmap(NULL, bytesToRead, PROT_READ, MAP_PRIVATE, fd, j*PAGE_SIZE);
        if (data == MAP_FAILED){
            std::cout << "Falló mmap\n";
            break;
        }

        int linesToSend = bytesToRead/sizeof(SampleLine);
        for (int i = 0; i < linesToSend; i++){
            //wait for 1 milisec
            usleep(1000);
            SampleLine sampleLine = data[i];
            //process
            sampleLine.process();
            //We should fix endianness here
            sampleLine.sendToSocket(streamingConnectionFd);
        }
        
        //unmap
        int unmapStatus = munmap(data, bytesToRead);
        helpers::throwErrorIf(unmapStatus < 0, "ERROR on munmap");

        accessController->incrementBytesRead(bytesToRead);

        bytesRead += bytesToRead;
        j++;
        }
    accessController->stopReading();
    std::cout << "Bytes read: " << bytesRead << "\n";
    std::cout << "n = " << j << "\n";
    close(fd);
    close(streamingConnectionFd);
    close(streamingSocketFd);
    std::cout << "Client: streaming socket closed\n";
    

}
//****End Client Class****//


void Server::handleClient(Client* client){
    std::cout << "Conectado!\n";

    int shmfd;
    std::string shmName;

    while(1){
        TLE tle = client->readTLE();
        bool isTLEValid = helpers::parseTLE(tle);
        helpers::writeNBytes(client->getSocketFd(), &isTLEValid, sizeof(isTLEValid));
        if (isTLEValid){
            std::cout << "TLE valido\n";
            float freq = client->readFreq();
            std::cout << "Frecuencia [MHz]: " << freq << "\n";

            //Debug. Next pass es ahora
            auto nextPass = std::chrono::system_clock::now();

            helpers::waitUntil(nextPass);

            std::string filename = tle.getName() + "_" + helpers::generateTimestamp();
            std::string filenameWithPath = "../captures/server_side/" + filename;
            client->setFilename(filename);
            std::cout << "Filename: " << filenameWithPath << "\n";

            //send an init flag to the client
            uint8_t initFlag = 1;
            helpers::writeNBytes(client->getSocketFd(), &initFlag, sizeof(initFlag));

            //create shared memory
            shmName = "/shm_" + filename;
            shmfd = shm_open(shmName.c_str(), O_RDWR | O_CREAT, 0666);
            helpers::throwErrorIf(shmfd < 0, "ERROR on shm_open");
            helpers::throwErrorIf(ftruncate(shmfd, sizeof(AccessController)) < 0, "ERROR on ftruncate");
            AccessController* accessController = (AccessController*) mmap(NULL, sizeof(AccessController), PROT_READ | PROT_WRITE, MAP_SHARED, shmfd, 0);
            helpers::throwErrorIf(accessController == MAP_FAILED, "ERROR on mmap");
            accessController->init();            
            
            pid_t pid = fork();
            helpers::throwErrorIf(pid == -1, "Error:: Fork failed");
            if(pid == 0){
                client->captureData(freq, tle, accessController);
                exit(0);
            }
            else{
                client->streamProcessedData(accessController);
            }
            break;
        }
        else{
            std::cout << "TLE invalido\n";         
        }
    }
    //unlink shm
    close(shmfd);
    int unlinkStatus = shm_unlink(shmName.c_str());
    helpers::throwErrorIf(unlinkStatus < 0, "ERROR on shm_unlink");
    std::cout << "Requesting to die\n";
    client->requestToDie();
    
    return;
}
