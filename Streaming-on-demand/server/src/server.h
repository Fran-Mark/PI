#pragma once
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include <thread>
#include <condition_variable>
#include <mutex>
#include <set>
#include <queue>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <arpa/inet.h>
#include "../../src/tle.h"
#include "../../src/sample.h"
#include <Beamformer.hpp>
#include "../../src/helpers.h"
#include <unistd.h>
#include "../../src/access_controller.h"
// class Server;

class Server{
    class Client{
        int socketFd;
        std::thread th;
        Server* server;
        std::string filename;
        std::string filenameWithPath;
    public:
        Client(int fd, Server* server_, void handler (Client* client));
        ~Client();
        int getSocketFd();
        TLE readTLE();
        float readFreq();
        void requestToDie();
        void captureData(float freq, TLE tle, AccessController* accessController);
        void launchCapturingThread(float freq, TLE tle);
        void streamProcessedData(AccessController* accessController);
        void setFilename(std::string filename_);
    };

    int socketFd;
    int portNo;
    sockaddr_in serverAddress;
    std::set<Client*> clients;
    std::mutex mutex;
    std::condition_variable cv;
    std::queue<Client*> clientsToKill;
    std::thread mainThread;
    std::thread cleanerThread;
    bool _isRunning;
    void setUpSocket();
    void cleanClients();
    void killAllClients();


public:
    Server(int portNo_);

    ~Server();

    void start();

    void stop();

    int getSocketFd();
    bool isRunning();

    void registerNewClients();
    static void handleClient(Client* client);

    void addClientToKill(Client* client);

};


