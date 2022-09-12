#include <signal.h>
#include <condition_variable>
#include "server.h"

std::condition_variable globalCv;
std::mutex globalMutex;
std::unique_lock<std::mutex> globalLk(globalMutex);
void catchSignal(int _){
    globalCv.notify_all();
}

int main(){
    Server server(2222);
    signal(SIGINT, catchSignal);
    server.start();
    globalCv.wait(globalLk);   
    server.stop();

    return 0;
}
