INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_MY_BEAMFORMER my_beamformer)

FIND_PATH(
    MY_BEAMFORMER_INCLUDE_DIRS
    NAMES my_beamformer/api.h
    HINTS $ENV{MY_BEAMFORMER_DIR}/include
        ${PC_MY_BEAMFORMER_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    MY_BEAMFORMER_LIBRARIES
    NAMES gnuradio-my_beamformer
    HINTS $ENV{MY_BEAMFORMER_DIR}/lib
        ${PC_MY_BEAMFORMER_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/my_beamformerTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(MY_BEAMFORMER DEFAULT_MSG MY_BEAMFORMER_LIBRARIES MY_BEAMFORMER_INCLUDE_DIRS)
MARK_AS_ADVANCED(MY_BEAMFORMER_LIBRARIES MY_BEAMFORMER_INCLUDE_DIRS)
