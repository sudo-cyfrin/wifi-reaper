import argparse
import subprocess
import os
import sys
from datetime import datetime

def ensure_output_dir():
    os.makedirs("output", exist_ok=True)

def log_filename(attack_name, bssid):
    clean_bssid = bssid.replace(":", "").lower()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"output/{attack_name}_{clean_bssid}_{timestamp}.log"

def run_with_logging(command_list, log_file):
    with open(log_file, "w") as f:
        process = subprocess.Popen(command_list, stdout=f, stderr=subprocess.STDOUT)
        process.communicate()

def enable_monitor(iface):
    subprocess.run(['python3', 'core/enable_monitor.py', iface])

def disable_monitor(iface):
    subprocess.run(['python3', 'core/disable_monitor.py', iface])

def run_scanner(iface):
    subprocess.run(['python3', 'core/scanner.py', iface])

def capture_handshake(bssid, channel, iface):
    ensure_output_dir()
    log_file = log_filename("handshake", bssid)
    run_with_logging(['python3', 'core/handshake.py', '--bssid', bssid, '--channel', channel, '--iface', iface], log_file)

def run_cracker(capture_file, wordlist):
    subprocess.run(['python3', 'core/cracker.py', '--capture', capture_file, '--wordlist', wordlist])

def run_pixie(bssid, iface):
    ensure_output_dir()
    log_file = log_filename("pixie", bssid)
    run_with_logging(['python3', 'core/pixie-dust.py', '--bssid', bssid, '--iface', iface], log_file)

def main():
    parser = argparse.ArgumentParser(
        description="WiFi Reaper Toolkit 🧟",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # UI Mode
    parser.add_argument("--ui", action="store_true", help="Launch menu-driven interface")

    # Monitor Mode Control
    parser.add_argument("-m", "--monitor", metavar="IFACE", help="Enable monitor mode on interface")
    parser.add_argument("-r", "--restore", metavar="IFACE", help="Disable monitor mode")

    # Scanning
    parser.add_argument("-s", "--scan", metavar="IFACE", help="Run Wi-Fi network scanner")

    # Attacks
    parser.add_argument("-H", "--handshake", action="store_true", help="Capture WPA/WPA2 handshake")
    parser.add_argument("-p", "--pixie", action="store_true", help="Run Pixie Dust WPS attack")
    parser.add_argument("-b", "--bssid", metavar="BSSID", help="Target BSSID for attack")
    parser.add_argument("-c", "--channel", metavar="CH", help="Channel number")
    parser.add_argument("-i", "--iface", metavar="IFACE", help="Wireless interface in monitor mode")

    # Cracking
    parser.add_argument("-C", "--crack", metavar="PCAP", help="Capture file to crack (.cap)")
    parser.add_argument("-w", "--wordlist", metavar="FILE", help="Wordlist to use for cracking")

    # Wordlist Builder
    parser.add_argument("-B", "--build-wordlist", action="store_true", help="Launch wordlist builder (cewl, crunch, cupp, wordlistctl)")

    args = parser.parse_args()

    if args.ui:
        from ui.menu import launch_main_menu
        launch_main_menu()
        sys.exit()

    if args.build_wordlist:
        from build_wordlist.menu import launch_menu
        launch_menu()
        sys.exit()

    if args.monitor:
        enable_monitor(args.monitor)

    elif args.restore:
        disable_monitor(args.restore)

    elif args.scan:
        run_scanner(args.scan)

    elif args.handshake:
        if args.bssid and args.channel and args.iface:
            capture_handshake(args.bssid, args.channel, args.iface)
        else:
            print("[-] --handshake requires --bssid, --channel, and --iface.")

    elif args.crack:
        if args.wordlist:
            run_cracker(args.crack, args.wordlist)
        else:
            print("[-] --crack requires --wordlist.")

    elif args.pixie:
        if args.bssid and args.iface:
            run_pixie(args.bssid, args.iface)
        else:
            print("[-] --pixie requires --bssid and --iface.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
