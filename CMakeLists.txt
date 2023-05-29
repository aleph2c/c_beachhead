cmake_minimum_required(VERSION 3.10)

# Set the project name
project (c_template)

# Glob the source files
file(GLOB SOURCES "src/*.c")

file(GLOB TESTS "test/*.c")

# Main executable
add_executable(hey main.c ${SOURCES})

target_include_directories( hey PUBLIC
    "${PROJECT_BINARY_DIR}"
    "${PROJECT_SOURCE_DIR}/inc"
)

# Test executable
enable_testing()
add_executable(tests ${SOURCES} ${TESTS})
target_include_directories( tests PRIVATE
    "${PROJECT_BINARY_DIR}"
    "${PROJECT_SOURCE_DIR}/inc"
    "${PROJECT_SOURCE_DIR}/test"
)
target_link_libraries(tests cmocka)
add_test(NAME hey_tests COMMAND tests)