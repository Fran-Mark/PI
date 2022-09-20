#include <signal.h>

#include "server.h"
#include <pybind11/embed.h>
#include <iostream>

bool _isActive;
// void catchSignal(int _){
//     _isActive = false;
// }

void run()
{
    Server server(2222);
    // signal(SIGINT, catchSignal);
    server.start();
    _isActive = true;
    std::string input;
    while (_isActive)
    {
        //read line
        std::getline(std::cin, input);   
        //std::cin >> input;
        std::cout << "You entered: " << input << std::endl;
        if (input == "stop")
        {
            _isActive = false;
        }
        if (input == "status")
        {
            std::cout << "Server is running" << std::endl;
            server.printStatus();
        }
    }
    server.stop();
}

void stop()
{
    _isActive = false;
}

PYBIND11_MODULE(streaming_server, m)
{
    m.doc() = "Server run on port 2222"; // optional module docstring
    m.def("run", &run, "runializes the server on port 2222");
    m.def("stop", &stop, "stops the server");
}
