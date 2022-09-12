#pragma once
#include <string>
#include <chrono>
#define TLE_LINE_LENGTH 69

class TLE{
    public:
        TLE(std::string name, std::string line1, std::string line2);
        ~TLE();
        std::string getLine1();
        std::string getLine2();
        std::string getName();
        std::string toString();
        static TLE parse(std::string tle);
        std::chrono::time_point<std::chrono::system_clock> getNextPass();
    private:
        std::string name;
        std::string line1;
        std::string line2;
        std::chrono::time_point<std::chrono::system_clock> nextPass;

};