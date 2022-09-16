#include <signal.h>

#include "server.h"
#include <pybind11/embed.h>
#include <iostream>

bool _isRunning;
void catchSignal(int _){
    _isRunning = false;
}

void run(){
    Server server(2222);
    signal(SIGINT, catchSignal);
    server.start();
    _isRunning = true;
    std::string input;
    while(_isRunning){
        std::cin >> input;
        if(input == "stop"){
            _isRunning = false;
        }
    }  
    server.stop();
}

PYBIND11_MODULE(streaming_server, m) {
    m.doc() = "Server run on port 2222"; // optional module docstring
    m.def("run", &run, "runializes the server on port 2222");
}
