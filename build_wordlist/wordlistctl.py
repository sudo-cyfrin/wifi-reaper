import subprocess

def run_wordlistctl():
    print("\n==[ WordlistCTL Interactive Mode ]==")
    print("[*] You will now enter the interactive shell of wordlistctl.")
    print("[*] Example usage once inside:\n")
    print("    > list categories")
    print("    > get passwords/rockyou -o output.txt\n")
    print("[*] To exit, type: exit\n")

    try:
        subprocess.run(["wordlistctl"])
    except FileNotFoundError:
        print("[!] wordlistctl not found. Install it with: pip install wordlistctl")
