#pragma once
#include <mutex>
#include <condition_variable>
#include <iostream>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include "./helpers.h"

#define PAGE_SIZE_IN_BYTES 4096

class AccessController{
    bool _isWriting;
    bool _isReading;
    long _bytesAvailable;
    long _bytesRead;
    int _fd;
    struct stat st;

    void _updateBytesAvailable();
public:
    void init();
    void setFd(int fd);
    void startWriting();
    void stopWriting();
    void startReading();
    void stopReading();
    void incrementBytesRead(int bytes);
    int getBytesToRead();
};