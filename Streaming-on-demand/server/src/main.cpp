#include <signal.h>
#include <condition_variable>
#include "server.h"
#include <pybind11/embed.h>

std::condition_variable globalCv;
std::mutex globalMutex;
std::unique_lock<std::mutex> globalLk(globalMutex);
void catchSignal(int _){
    globalCv.notify_all();
}

// int main(int argc, char* argv[]){
//     Server server(2222);
//     signal(SIGINT, catchSignal);
//     server.start();
//     globalCv.wait(globalLk);   
//     server.stop();

//     return 0;
// }

void init(){
    Server server(2222);
    signal(SIGINT, catchSignal);
    server.start();
    globalCv.wait(globalLk);   
    server.stop();
}

PYBIND11_MODULE(streaming_server, m) {
    m.doc() = "Server init on port 2222"; // optional module docstring
    m.def("init", &init, "Initializes the server on port 2222");
}
