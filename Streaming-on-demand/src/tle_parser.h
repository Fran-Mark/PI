#pragma once
#include "helpers.h"
#include <pybind11/embed.h>
#include "tle.h"
#include <iostream>
#include <chrono>

#define ERROR_TIME_POINT std::chrono::time_point<std::chrono::system_clock>(std::chrono::system_clock::duration::max())

std::chrono::time_point<std::chrono::system_clock> getNextPass(TLE tle);
std::chrono::time_point<std::chrono::system_clock> stringToTimePoint(std::string timeString);