# GNU Radio C++ Flow Graph CMakeLists.txt
#
# Title: Entendiendo file sink
# Author: fran
# GNU Radio version: 3.8.4.0


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

add_executable(output_test output_test.cpp)
target_link_libraries(output_test ${GR_LIBRARIES})
