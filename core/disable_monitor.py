import subprocess

def list_wireless_interfaces():
    result = subprocess.run(['iw', 'dev'], capture_output=True, text=True)
    interfaces = []
    for line in result.stdout.splitlines():
        if line.strip().startswith("Interface"):
            iface = line.strip().split()[1]
            interfaces.append(iface)
    return interfaces

import subprocess

def disable_monitor(iface):
    print(f"[+] Bringing down {iface}...")
    subprocess.run(['ip', 'link', 'set', iface, 'down'])

    print(f"[+] Setting managed mode...")
    subprocess.run(['iw', iface, 'set', 'type', 'managed'])

    print(f"[+] Bringing up {iface}...")
    subprocess.run(['ip', 'link', 'set', iface, 'up'])

    print(f"[✔] {iface} is now in managed mode!")

    restart = input("Do you want to restart NetworkManager and wpa_supplicant? (Recommended)(y/n): ").lower()
    if restart == 'y':
        print("[*] Restarting NetworkManager and wpa_supplicant...")
        subprocess.run(['systemctl', 'restart', 'NetworkManager'])
        subprocess.run(['systemctl', 'restart', 'wpa_supplicant'])
        print("[✔] Services restarted.")

if __name__ == "__main__":
    iface = input("Enter interface to disable monitor mode: ").strip()
    disable_monitor(iface)

