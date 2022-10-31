#include "tle_parser.h"
namespace py = pybind11;
using namespace py::literals;

time_point<system_clock> TLEParser::stringToTimePoint(std::string timeString)
{
    std::tm tm = {};

    tm.tm_year = std::stoi(timeString.substr(0, 4)) - 1900;
    tm.tm_mon = std::stoi(timeString.substr(5, 2)) - 1;
    tm.tm_mday = std::stoi(timeString.substr(8, 2));
    tm.tm_hour = std::stoi(timeString.substr(11, 2));
    tm.tm_min = std::stoi(timeString.substr(14, 2));
    tm.tm_sec = std::stoi(timeString.substr(17, 2));

    std::time_t t = std::mktime(&tm);
    return system_clock::from_time_t(t);
}
time_point<system_clock> TLEParser::getNextPass(TLE tle)
{
    py::gil_scoped_release release;
    py::gil_scoped_acquire acquire;
    try
    {
        py::module_ tle_parser = py::module::import("tle_parser");
        py::object result = tle_parser.attr("getNextPass")(tle.getLine1(), tle.getLine2());
        std::string res = result.cast<std::string>();
        std::cout << res << std::endl;
        return TLEParser::stringToTimePoint(res);
    }
    catch (py::error_already_set const &e)
    {   
        std::cout << "Error in python script" << std::endl;
        return ERROR_TIME_POINT;
    }
}
