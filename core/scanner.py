from scapy.all import *
import time

# Store discovered APs
networks = {}

def callback(packet):
    if packet.haslayer(Dot11Beacon) or packet.haslayer(Dot11ProbeResp):
        bssid = packet[Dot11].addr2
        ssid = packet[Dot11Elt].info.decode(errors='ignore') if packet[Dot11Elt].info else 'Hidden'
        stats = packet[Dot11Beacon].network_stats() if packet.haslayer(Dot11Beacon) else packet[Dot11ProbeResp].network_stats()
        channel = stats.get("channel", "N/A")
        crypto = stats.get("crypto", ["N/A"])[0]
        signal = packet.dBm_AntSignal if hasattr(packet, "dBm_AntSignal") else "N/A"

        if bssid not in networks:
            networks[bssid] = {
                "SSID": ssid,
                "Channel": channel,
                "Signal": signal,
                "Encryption": crypto
            }
            print(f"[+] {ssid} | {bssid} | CH: {channel} | Signal: {signal} | {crypto}")

def scanner(iface):
    print(f"[+] Scanning for networks on {iface}... Press Ctrl+C to stop. (Wait ~30s for better results)\n")
    try:
        sniff(iface=iface, prn=callback, store=0)
    except KeyboardInterrupt:
        print("\n\n[✔] Scan complete. Found networks:\n")
        print("{:<20} {:<20} {:<8} {:<8} {:<10}".format("SSID", "BSSID", "Channel", "Signal", "Encryption"))
        print("-" * 75)
        for bssid, info in networks.items():
            print("{:<20} {:<20} {:<8} {:<8} {:<10}".format(info['SSID'], bssid, info['Channel'], info['Signal'], info['Encryption']))
        print("\n[+] Done.")

# Optional: test run when directly executed
if __name__ == "__main__":
    iface = input("Enter interface in monitor mode (e.g., wlan0mon): ").strip()
    scanner(iface)
