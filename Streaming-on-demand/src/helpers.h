#pragma once
#include <stdlib.h>
#include <stdio.h>
#include <chrono>
#include <thread>
#include <netinet/in.h>
#include <sys/types.h>          /* See NOTES */
#include <sys/socket.h>
#include "../src/tle.h"
#include "../src/sample.h"
#include <unistd.h>
#include <strings.h>
#include <iostream>
namespace helpers
{
    void throwErrorIf(bool cond, const char *msg);
    void waitUntil(std::chrono::time_point<std::chrono::system_clock> timePoint);
    bool parseTLE(TLE tle);
    void readNBytes(int fd,void* buffer, size_t nBytes);
    void writeNBytes(int fd, void* message, size_t nBytes);
    std::string generateTimestamp();
} // namespace helpers

