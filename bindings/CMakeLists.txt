cmake_minimum_required(VERSION 3.15)
project(midshake_cpp LANGUAGES CXX)

# Use C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# MSYS2 MinGW64 pybind11 + Python
set(CMAKE_PREFIX_PATH "C:/msys64/mingw64")

# Find pybind11 (installed via pacman)
find_package(pybind11 REQUIRED)

# Find Python (MSYS2 MinGW64 version)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

# Include your engine headers
include_directories(
    ${PROJECT_SOURCE_DIR}/../cpp
)

# Build the Python module
pybind11_add_module(midshake_cpp
    midshake_bindings.cpp
    ../cpp/midshake_engine.cpp
)

# Link Python
target_link_libraries(midshake_cpp PRIVATE Python3::Python)
