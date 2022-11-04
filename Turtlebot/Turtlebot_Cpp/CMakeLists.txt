project(paho_cpp_example)

cmake_minimum_required(VERSION 3.10)

# Find the PahoMqttCpp package
find_package(PahoMqttCpp REQUIRED)

include_directories("inc")

add_executable(cpp_example cpp_example.cpp)
target_link_libraries(cpp_example PahoMqttCpp::paho-mqttpp3)
