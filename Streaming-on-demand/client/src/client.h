#pragma once
#include <netinet/in.h>
#include <iostream>       
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/socket.h>
#include <netdb.h> 
#include "../../src/helpers.h"

#define SAMPLE_LINE_LENGTH 128
class Client {
    private:
        int socketFd;
        struct sockaddr_in serverAddress;
        struct hostent *server;

    public:
        Client(char *hostname, int port);
        ~Client();
        void run();
        void sendMessage(void* msg,int nBytes);
        void receiveData(int port);
};