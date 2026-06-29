from logic.organiser import organize
from time import sleep
from logic.utils import main_drives
from logic.nav import directory
        
if __name__ == "__main__":
    print(f"{" ":<12}{"\033[1;92mSTARTUP SUCCESSFUL!!\033[0m"}")
    sleep(0.5)
    current = 0
    selected_folder = 0
    while True:
        current = main_drives()
        print(f"{" ":<12}{"\033[1;95mPlease Wait...\033[0m"}")
        print("\n")
        sleep(0.5)

        selected_folder = directory(current)
        print(f"{" ":<12}{"\033[1;95mPlease Wait...\033[0m"}")
        print("\n")
        sleep(0.5)

        if selected_folder == "Drive Menu":
            continue #Goes back to the drive menu
        
        break

