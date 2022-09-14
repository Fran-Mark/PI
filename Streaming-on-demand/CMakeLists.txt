cmake_minimum_required(VERSION 3.13)
project(Marquinez-tp-redes)


# SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread -lrt")


# set(CLIENT_CPPS "client/src/client.cpp" "src/helpers.cpp" "src/tle.cpp" "client/src/main.cpp" "src/sample.cpp")
# add_executable(client ${CLIENT_CPPS})

# set(SERVER_CPPS "server/src/server.cpp" "src/helpers.cpp" "src/tle.cpp" "server/src/main.cpp" "src/sample.cpp" "src/access_controller.cpp")

# add_executable(server ${SERVER_CPPS})

# find_library(LIBRT rt) 
# if(LIBRT)
# target_link_libraries(server ${LIBRT})
# endif()
# target_link_libraries(server Beamformer)
# add_subdirectory(gnuradio)

set(CMAKE_CXX_STANDARD 14)
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pthread -lrt")

include(FetchContent)
FetchContent_Declare(
	pybind11
	GIT_REPOSITORY https://github.com/pybind/pybind11.git
	GIT_TAG        v2.6.2
	GIT_SHALLOW    TRUE
)

FetchContent_MakeAvailable(pybind11)

set(CLIENT_CPPS "client/src/client.cpp" "src/helpers.cpp" "src/tle.cpp" "client/src/main.cpp" "src/sample.cpp")
set(SERVER_CPPS "server/src/server.cpp" "src/helpers.cpp" "src/tle.cpp" "server/src/main.cpp" "src/sample.cpp" "src/access_controller.cpp")

#add_subdirectory(pybind11)

set(TARGET_NA)

pybind11_add_module(streaming_server ${SERVER_CPPS})
target_compile_features(streaming_server PUBLIC cxx_std_14)
set_target_properties(${target_name} PROPERTIES SUFFIX ".so")

pybind11_add_module(streaming_client ${Client_CPPS})
target_compile_features(streaming_client PUBLIC cxx_std_14)
set_target_properties(streaming_client PROPERTIES SUFFIX ".so")

find_library(LIBRT rt) 
if(LIBRT)
target_link_libraries(${target_name} ${LIBRT})
endif()
target_link_libraries(${target_name} Beamformer)
add_subdirectory(gnuradio)
