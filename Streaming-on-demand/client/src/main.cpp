#include "client.h"
#include <pybind11/embed.h>

// int main(int argc, char *argv[])
// {
//     int portNo;
//     struct sockaddr_in serverAddress;
//     char* hostname;

    
//     if (argc < 3) {
//        fprintf(stderr,"usage %s hostname port\n", argv[0]);
//        exit(0);
//     }
//     portNo = atoi(argv[2]);
//     hostname = argv[1];
//     Client client(hostname, portNo);

//     client.run();    
    
//     return 0;
// }

void init(){
    int portNo = 2222;
    struct sockaddr_in serverAddress;
    char* hostname = "localhost";

    Client client(hostname, portNo);

    client.run();  
}

PYBIND11_MODULE(streaming_client, m) {
    m.doc() = "client init on port 2222"; // optional module docstring
    m.def("init", &init, "Initializes the client on port 2222");
}