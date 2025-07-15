def launch_menu():
    print("==[ Wordlist Builder Menu ]==")
    print("1. CEWL - Scrape from website")
    print("2. Crunch - Generate brute-force list")
    print("3. CUPP - Social-engineered wordlist")
    print("4. WordlistCTL - Download prebuilt list")
    print("5. Exit")

    choice = input("\nChoose an option [1-5]: ").strip()

    if choice == "1":
        from build_wordlist.cewl import run_cewl
        run_cewl()
    elif choice == "2":
        from build_wordlist.crunch import run_crunch
        run_crunch()
    elif choice == "3":
        from build_wordlist.cupp import run_cupp
        run_cupp()
    elif choice == "4":
        from build_wordlist.wordlistctl import run_wordlistctl
        run_wordlistctl()
    else:
        print("Byee")
