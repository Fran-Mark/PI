#include "client.h"

int main(int argc, char *argv[])
{
    int portNo;
    struct sockaddr_in serverAddress;
    char* hostname;

    
    if (argc < 3) {
       fprintf(stderr,"usage %s hostname port\n", argv[0]);
       exit(0);
    }
    portNo = atoi(argv[2]);
    hostname = argv[1];
    Client client(hostname, portNo);

    client.run();    
    
    return 0;
}
