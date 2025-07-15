from core import enable_monitor
from core import disable_monitor
from core import scanner
from core import handshake
from core import cracker
from core import pixie_dust
from build_wordlist.menu import launch_menu

def launch_main_menu():
    while True:
        print("\n==[ WiFi Reaper Toolkit 🧟 Main Menu ]==")
        print("1. Enable Monitor Mode")
        print("2. Disable Monitor Mode")
        print("3. Scan Wi-Fi Networks")
        print("4. Capture WPA Handshake")
        print("5. Crack Handshake with Wordlist")
        print("6. Run Pixie Dust Attack (WPS)")
        print("7. Build Wordlist")
        print("8. Exit")

        choice = input("Select an option [1-8]: ").strip()

        if choice == "1":
            iface = input("Enter interface name: ").strip()
            enable_monitor.main(iface)

        elif choice == "2":
            iface = input("Enter interface name: ").strip()
            disable_monitor.main(iface)

        elif choice == "3":
            scanner.main()

        elif choice == "4":
            handshake.main()

        elif choice == "5":
            cracker.main()

        elif choice == "6":
            pixie_dust.main()

        elif choice == "7":
            launch_menu()

        elif choice == "8":
            print("Goodbye! Stay spooky 🧟")
            break

        else:
            print("[!] Invalid choice. Try again.")
