#include <iostream>
#include <string>

class Scanner {
public:
    void runDiscovery(std::string targetIp) {
        std::cout << "\033[1;31m[Recon]\033[0m Scanning ports on " << targetIp << "..." << std::endl;
        // Logic: Wraps nmap command or custom TCP syn scanner
        std::string cmd = "nmap -sS -T4 " + targetIp;
        system(cmd.c_str());
    }
};