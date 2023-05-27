cmake_minimum_required(VERSION 3.10)

# Set the project name
project (c_template)


# add an include path
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/inc)

# Add the executable
add_executable( hey ${CMAKE_CURRENT_SOURCE_DIR}/src/hey.c)