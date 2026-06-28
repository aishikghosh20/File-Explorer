from time import sleep
from pathlib import Path
from .folder_check import should_skip
import os, subprocess

def clear(): # To clear the screen
    os.system("cls")
    sleep(0.2)
    # subprocess.run("cls" if os.name == "nt" else "clear", shell= True)
    
  
def title():
    # menu
    print("\033[36m==========================================")
    print("\033[1;97m             FILE MANAGER \033[0m")
    print("\033[36m==========================================\033[0m")
   
def exit_app():
    print(f"\033[1;93mExiting the program...\033[0m")
    sleep(1)
    print("\n\033[1;95m!!Thank you for using!!\033[0m")
    sleep(0.5)
    print("\033[1;95mCoded by: Aishik Ghosh\033[0m")
    sleep(0.5)
    input("\nPress Enter to Exit...")
    exit()


def options():
    print("\033[1;36m1 : Organize Files\n2 : Delete Files\n3 : ⬅️  Go Back\n4 : Exit \033[0m\n")
    valid = False
    while not(valid):
        try:
            choice = int(input("\033[1;97mEnter a choice:\033[0m\n"))
        except ValueError:
            print("\033[1;91mENTER A VALID INPUT\033[0m\n")
            sleep(0.5)
            continue
        if (1<=choice<=4):
            valid = True
        else:
            print("\033[1;91mENTER A VALID CHOICE\033[0m\n")
            sleep(0.5)
    return choice


def main_drives():
    print(f"\033[1;97mAvailable Drives\033[0m")
    # Fetches and lists the system drives
    drives = []
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        drive = Path(f"{letter}:/")
        if drive.exists():
            drives.append(drive)
    last_index = 0

    # Prints them
    for index, folder in enumerate(drives,start=1):
        print(f"{" ":<3}{f"{index}.":<5}{f"📁 {folder}"}")
        last_index = index
        sleep(0.1)
    
    last_index+=1
    print(f"{" ":<3}{f"{last_index}.":<5}{f"Exit"}")

    sleep(0.3)
    # Prompt for user's choice
    valid = False
    while not(valid):
        try:
            choice = int(input("\033[1;93mChoose a drive :\033[0m\n"))
        except ValueError:
            print("\033[1;91mENTER A VALID INPUT\033[0m\n")
            sleep(0.5)
            continue
        if (1<=choice<=last_index):
            valid = True
        else:
            print(f"\033[1;91mENTER A VALID BETWEEN 1 AND {last_index}\033[0m\n")
            sleep(0.5)

    if choice == last_index:
        exit_app()

    current = drives[choice-1]
    return current
    
def format_size(size):
    if size <1024:
        return f"{f"{size}":<5} B"
    elif size<1024**2:
        return f"{f"{size/1024:.3f}":<5} KB"
    elif size<1024**3:
        return f"{f"{size/1024**2:.3f}":<5} MB"
    elif size<1024**4:
        return f"{f"{size/1024**3:.3f}":<5} GB"
    else:
        return f"{f"{size/1024**4:.3f}":<5} TB"


def directory(drive):
    current = drive # Fetches the current directory
    while True:
        clear()
        title()
        print(f"{"\033[1;93m📂CURRENT DIRECTORY:\033[0m\n":<10}{f"\033[1;97m{current}\033[0m"}")
        print("\033[36m==========================================\033[0m")
        sleep(0.3)
        folders = [items for items in current.iterdir()]


        visible_items= []
        # To remove system folders and protected folders from the list
        for items in folders:
            if items.is_dir() & should_skip(items):
                continue
            visible_items.append(items)

        last_index = 0 
        for index, subitem in enumerate(visible_items, start=1):
            if subitem.is_dir():
                print(f"{" ":<3}{f"{index}.":<5}{f"📁 {subitem.name}"}")
                last_index = index
                sleep(0.1)
            else:
                size = subitem.stat().st_size
                formatted_size = format_size(size)
                print(f"{" ":<3}{f"{index}.":<5}{f"📃 {subitem.name}":<40}{f"{formatted_size}"}")
                sleep(0.1)
        
        visible_items.append("✔️  Select This Folder")
        visible_items.append("⬅️  Go Back")
        
        sleep(0.4)
        print("\033[36m==========================================\033[0m")
        for index, subitem in enumerate(visible_items[last_index:], start=last_index+1):         
            if not isinstance(subitem,(Path)) or not subitem.is_file():
                last_index = index
                print(f"{" ":<3}{f"{index}.":<5}{f"{subitem}"}")
                sleep(0.1)
        
        print(f"\n{" ":<12}{"\033[1;93mSELECTED A FOLDER TO PERFORM ACTIONS\033[0m":<10}")
        sleep(0.5)
        choice=0
        # Prompt for user's choice
        valid = False
        while not(valid):
            try:
                choice = int(input("\033[1;93mChoose :\033[0m\n"))
            except ValueError:
                print("\033[1;91mENTER A VALID INPUT\033[0m\n")
                sleep(0.5)
                continue
            if (1<=choice<=last_index):
                valid = True
            else:
                print(f"\033[1;91mENTER A VALID BETWEEN 1 AND {last_index}\033[0m\n")
                sleep(0.5)

        selected = visible_items[choice-1]

        if isinstance(selected, Path) and selected.is_dir(): # If a folder is opened
            current = selected
            continue

        elif selected == "⬅️  Go Back": # If go back is selected
            if current.parent != current:
                current = current.parent
            continue # This redraws the previous directory

        elif selected == "✔️  Select This Folder": # If a folder is selected 
            return current
        
        