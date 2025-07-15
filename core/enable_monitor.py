import subprocess

def list_wireless_interfaces():
    result = subprocess.run(['iw', 'dev'], capture_output=True, text=True)
    interfaces = []
    for line in result.stdout.splitlines():
        if line.strip().startswith("Interface"):
            iface = line.strip().split()[1]
            interfaces.append(iface)
    return interfaces

def enable_monitor(iface):
    print(f"[+] Bringing down {iface}...")
    subprocess.run(['ip', 'link', 'set', iface, 'down'])

    print(f"[+] Setting monitor mode...")
    subprocess.run(['iw', iface, 'set', 'monitor', 'control'])

    print(f"[+] Bringing up {iface}...")
    subprocess.run(['ip', 'link', 'set', iface, 'up'])

    print(f"[✔] {iface} is now in monitor mode!")

if __name__ == "__main__":
    iface = input("Enter interface to enable monitor mode: ").strip()
    enable_monitor(iface)
