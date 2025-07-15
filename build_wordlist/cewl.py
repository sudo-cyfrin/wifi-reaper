import subprocess
import os

def run_cewl():
    print("\n==[ CEWL Wordlist Builder ]==")
    url = input("Enter target URL (e.g., https://example.com): ").strip()
    output = input("Enter output file path [default: data/wordlists/cewl.txt]: ").strip()
    
    if not output:
        output = "data/wordlists/cewl.txt"

    os.makedirs(os.path.dirname(output), exist_ok=True)

    print(f"[+] Running cewl on {url}...")
    try:
        subprocess.run(["cewl", url, "-w", output])
        print(f"[✔] Wordlist saved to: {output}")
    except FileNotFoundError:
        print("[!] cewl not found. Please install it using: sudo apt install cewl")
