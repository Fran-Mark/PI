#include "access_controller.h"

void AccessController::init(){
    _isWriting = false;
    _isReading = false;
    _bytesAvailable = 0;
}

void AccessController::setFd(int fd){
    _fd = fd;
}

void AccessController::startWriting(){
    _isWriting = true;
}

void AccessController::stopWriting(){
    _isWriting = false;
    std::cout << "Stopped writing" << std::endl;
}

void AccessController::startReading(){
    while(_isWriting == false){
        std::cout << "Waiting for writer before reading..." << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    _isReading = true;
    std::cout << "Starting to read..." << std::endl;
}

void AccessController::stopReading(){
    _isReading = false;
    std::cout << "Stopped reading" << std::endl;
}


void AccessController::incrementBytesRead(int bytes){
    _bytesRead += bytes;
}

void AccessController::_updateBytesAvailable(){
    helpers::throwErrorIf(_fd == -1, "AccessController::_updateBytesAvailable: _fd is -1");
    helpers::throwErrorIf(fstat(_fd, &st) < 0, "ERROR getting file size");
    int fileSize = st.st_size;
    _bytesAvailable = fileSize - _bytesRead;
}

int AccessController::getBytesToRead(){
    _updateBytesAvailable();
    if (_bytesAvailable >= PAGE_SIZE_IN_BYTES){
        return PAGE_SIZE_IN_BYTES;
    }
    if (!_isWriting){
        return _bytesAvailable;
    }
    std::cout << "Waiting for bytes to read..." << std::endl;
    usleep(100000);
    return getBytesToRead();
}