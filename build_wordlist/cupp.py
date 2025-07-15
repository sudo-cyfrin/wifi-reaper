import subprocess
import os

def run_cupp():
    print("\n==[ CUPP Wordlist Builder ]==")
    print("[*] Launching interactive CUPP (Common User Passwords Profiler)...")

    # Optional: Ask if user wants to save to a custom location
    custom_output = input("Do you want to specify an output location? (y/N): ").strip().lower()
    
    if custom_output == "y":
        output_path = input("Enter output file path [e.g., data/wordlists/custom_cupp.txt]: ").strip()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        try:
            subprocess.run(["cupp", "-i", "-o", output_path])
            print(f"[✔] Wordlist saved to: {output_path}")
        except FileNotFoundError:
            print("[!] cupp not found. Install it or run: git clone https://github.com/Mebus/cupp.git")
    else:
        try:
            subprocess.run(["cupp", "-i"])
        except FileNotFoundError:
            print("[!] cupp not found. Install it or run: git clone https://github.com/Mebus/cupp.git")
