#pragma once
#include "helpers.h"
#include <pybind11/embed.h>
#include "tle.h"
#include <iostream>
#include <chrono>

#define ERROR_TIME_POINT std::chrono::time_point<std::chrono::system_clock>(std::chrono::system_clock::duration::max())

using namespace std::chrono;
namespace TLEParser
{
time_point<system_clock> getNextPass(TLE tle);
time_point<system_clock> stringToTimePoint(std::string timeString);
}