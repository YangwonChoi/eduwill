cmake_minimum_required(VERSION 3.22)
project(untitled3)

set(CMAKE_CXX_STANDARD 14)

add_executable(untitled3 main.cpp sqlite3.c)
target_link_libraries(untitled3 -ldl -lpthread)
