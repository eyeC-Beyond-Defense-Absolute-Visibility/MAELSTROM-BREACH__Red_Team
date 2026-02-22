#!/bin/bash
echo -e "\033[1;31mStarting Maelstrom-Breach Orchestrator...\033[0m"

# Build the C2
mkdir -p build && cd build
cmake .. && make
cd ..

# Execute the Beta Campaign
./build/Maelstrom --campaign configs/campaign_beta.json