# GNU Radio C++ Flow Graph CMakeLists.txt
#
# Title: Not titled yet
# Author: fran
# GNU Radio version: v3.8.5.0-6-g57bd109d


cmake_minimum_required(VERSION 3.8)


include_directories(
    ${GNURADIO_ALL_INCLUDE_DIRS}
    ${Boost_INCLUDE_DIRS}
    $ENV{HOME}/.grc_gnuradio
)




set(GR_LIBRARIES
    boost_system
    gnuradio-blocks
    gnuradio-runtime
    gnuradio-pmt
    log4cpp
)

add_executable(main_cpp main_cpp.cpp)
target_link_libraries(main_cpp ${GR_LIBRARIES})
