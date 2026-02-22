cmake_minimum_required(VERSION 3.10)
project(MaelstromBreach)

set(CMAKE_CXX_STANDARD 17)

add_executable(Maelstrom src/main.cpp src/modules/Scanner.cpp src/modules/ExploitEngine.cpp)
add_executable(RansomSim src/payloads/ransom_sim.cpp)