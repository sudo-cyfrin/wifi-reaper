import subprocess
import os

def run_crunch():
    print("\n==[ Crunch Wordlist Builder ]==")
    
    try:
        min_len = int(input("Enter minimum length: ").strip())
        max_len = int(input("Enter maximum length: ").strip())
    except ValueError:
        print("[-] Invalid length input. Must be integers.")
        return

    charset = input("Enter character set (e.g., abc123@#): ").strip()
    output = input("Enter output file path [default: data/wordlists/crunch.txt]: ").strip()

    if not output:
        output = "data/wordlists/crunch.txt"

    os.makedirs(os.path.dirname(output), exist_ok=True)

    print(f"[+] Generating wordlist with crunch...")
    try:
        subprocess.run(["crunch", str(min_len), str(max_len), charset, "-o", output])
        print(f"[✔] Wordlist saved to: {output}")
    except FileNotFoundError:
        print("[!] crunch not found. Install it using: sudo apt install crunch")
