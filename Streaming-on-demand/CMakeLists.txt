project(Marquinez-tp-redes)
cmake_minimum_required(VERSION 3.8)

SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread -lrt")


set(CLIENT_CPPS "client/src/client.cpp" "src/helpers.cpp" "src/tle.cpp" "client/src/main.cpp" "src/sample.cpp")
add_executable(client ${CLIENT_CPPS})

set(SERVER_CPPS "server/src/server.cpp" "src/helpers.cpp" "src/tle.cpp" "server/src/main.cpp" "src/sample.cpp" "src/access_controller.cpp")

add_executable(server ${SERVER_CPPS})

find_library(LIBRT rt) 
if(LIBRT)
target_link_libraries(server ${LIBRT})
endif()
target_link_libraries(server Beamformer)
add_subdirectory(gnuradio)