#include "tle.h"
#include <sstream>

TLE::TLE(std::string name, std::string line1, std::string line2) {
    this->name = name;
    this->line1 = line1;
    this->line2 = line2;
}
TLE::~TLE() {
}
std::string TLE::toString() {
    return this->name + "\n" + this->line1 + "\n" + this->line2;
}

TLE TLE::parse(std::string tle) {
    std::string name;
    std::string line1;
    std::string line2;
    std::stringstream ss(tle);
    std::getline(ss, name, '\n');
    std::getline(ss, line1, '\n');
    std::getline(ss, line2, '\n');
    return TLE(name, line1, line2);
}

std::chrono::time_point<std::chrono::system_clock> TLE::getNextPass() {
    return nextPass;
}

std::string TLE::getLine1() {
    return this->line1;
}
std::string TLE::getLine2() {
    return this->line2;
}

std::string TLE::getName() {
    return this->name;
}