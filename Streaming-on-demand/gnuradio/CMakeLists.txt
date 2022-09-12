# GNU Radio C++ Flow Graph CMakeLists.txt
#
# Title: Beamformer
# Author: fran
# GNU Radio version: 3.8.4.0


cmake_minimum_required(VERSION 3.8)


include_directories(
    ${GNURADIO_ALL_INCLUDE_DIRS}
    ${Boost_INCLUDE_DIRS}
    ${GNURADIO_RUNTIME_INCLUDE_DIRS}
    $ENV{HOME}/.grc_gnuradio
    .
)

set(GR_LIBRARIES
boost_system
    gnuradio-blocks
    gnuradio-runtime
    gnuradio-pmt
    log4cpp
    gnuradio-filter
    )
    
add_library(Beamformer Beamformer.cpp)
target_link_libraries(Beamformer ${GR_LIBRARIES})
target_include_directories(Beamformer PUBLIC .)
