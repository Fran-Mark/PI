#pragma once
#include <stdint.h>
#include <complex>
#include <array>
#include <string>
#include <string.h>
#include <iostream>
#include "./helpers.h"
struct SampleLine{
    std::array<std::complex<float>, 16> data;
    char* serialize();
    void sendToSocket(int socketFd);
    void process();
};
