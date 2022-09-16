#include "helpers.h"

void helpers::throwErrorIf(bool cond, const char *msg){
    if(cond){
        perror(msg);
        exit(1);
    }
}

void helpers::waitUntil(std::chrono::time_point<std::chrono::system_clock> timePoint){
    std::chrono::duration<double> timeDiff = timePoint - std::chrono::system_clock::now();
    if(timeDiff.count() > 0){
        std::cout << "Waiting for " << timeDiff.count() << " seconds" << std::endl;
        std::this_thread::sleep_for(timeDiff);
    }
}

void helpers::readNBytes(int fd, void* buffer, size_t nBytes){
    size_t bytesRead = 0;
    char buf[nBytes];
    bzero(buf, nBytes);

    while(bytesRead < nBytes){
        size_t n = read(fd, buf + bytesRead, nBytes - bytesRead);
        helpers::throwErrorIf(n < 0 && errno != EINTR, "ERROR reading from socket");
        if (n == 0){
            std::cout << "Socket closed\n";
            break;
        }    
        
        bytesRead += n;
    }
    memcpy(buffer, buf, nBytes);
}



void helpers::writeNBytes(int fd, void* message, size_t nBytes){
    ssize_t bytesWritten = 0;
    while(bytesWritten < nBytes){
        ssize_t n = write(fd, (char*)message + bytesWritten, nBytes - bytesWritten);
        helpers::throwErrorIf(n < 0 && errno != EINTR, "ERROR writing to socket");
        if (n == 0){
            std::cout << "Socket closed\n";
            break;
        }
        bytesWritten += n;
    }
}


std::string helpers::generateTimestamp(){
    time_t t = time(0);
    std::string s(30, '\0');
    std::strftime(&s[0], s.size(), "%Y-%m-%d_%H-%M-%S", std::localtime(&t));
    return s;

   // timestamp += std::to_string(now->tm_year + 1900) + "-" ; 
}