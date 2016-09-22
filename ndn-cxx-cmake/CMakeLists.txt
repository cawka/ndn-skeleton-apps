cmake_minimum_required (VERSION 3.1)

set (CMAKE_CXX_STANDARD 11)

INCLUDE (FindPkgConfig)
pkg_check_modules (NDN_CXX libndn-cxx)

project (server)
add_executable (server server.cpp)

include_directories(server ${NDN_CXX_INCLUDE_DIRS})
link_directories(server ${NDN_CXX_LIBRARY_DIRS} )
target_link_libraries(server ${NDN_CXX_LIBRARIES})


add_executable (client server.cpp)

include_directories(client ${NDN_CXX_INCLUDE_DIRS})
link_directories(client ${NDN_CXX_LIBRARY_DIRS} )
target_link_libraries(client ${NDN_CXX_LIBRARIES})
