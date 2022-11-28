project(main)

cmake_minimum_required(VERSION 3.10)

# Find the PahoMqttCpp package
find_package(PahoMqttCpp REQUIRED)

include_directories("inc")

add_executable(main main.cpp)
target_link_libraries(main PahoMqttCpp::paho-mqttpp3)
