from logic.organiser import organize
from pathlib import Path
from time import sleep
from logic.utils import directory, title, exit_app, main_drives, options, clear
        
if __name__ == "__main__":
    print(f"{" ":<12}{"\033[1;92mSTARTUP SUCCESSFUL!!\033[0m"}")
    sleep(0.5)
    title()
    sleep(0.3)
    current = main_drives()
    print(f"{" ":<12}{"\033[1;95mPlease Wait...\0323[0m"}")
    print("\n")
    sleep(0.5)
    selected_folder = directory(current)
    print(f"{" ":<12}{"\033[1;95mPlease Wait...\033[0m"}")
    print("\n")
    sleep(0.5)
    clear()
    title()
    print(f"{"\033[1;93m📂CURRENT DIRECTORY:\033[0m\n":<10}{f"\033[1;97m{selected_folder}\033[0m"}")
    print("\033[36m==========================================\033[0m")
    choice = options()
    if choice == 4:
        exit_app()
    elif choice == 3:
        sleep(0.3)
        directory (selected_folder.parent)
        
