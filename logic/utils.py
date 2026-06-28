from time import sleep
from pathlib import Path
from .folder_check import should_skip
import os

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
    print("\n\033[1;95m!!😊Thank you for using!!\033[0m")
    sleep(0.5)
    print("\033[1;95mCoded by: \033[1;97mAishik Ghosh\033[0m")
    sleep(0.5)
    input("\nPress Enter to Exit...")
    exit()


def main_drives():
    clear()
    title()
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
    print(f"{" ":<3}{f"{last_index}.":<5}{f"❌  Exit"}")

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

    if choice == "❌  Exit":
        exit_app()

    current = drives[choice-1]
    return current

FILE_ICONS = {
    ".txt": "📄",
    ".pdf": "📕",
    ".doc": "📝",
    ".docx": "📝",
    ".mp3": "🎵",
    ".wav": "🎵",
    ".flac": "🎵",
    ".mp4": "🎬",
    ".mkv": "🎬",
    ".avi": "🎬",
    ".jpg": "🖼️",
    ".jpeg": "🖼️",
    ".png": "🖼️",
    ".gif": "🖼️",
    ".zip": "🗜️",
    ".rar": "🗜️",
    ".7z": "🗜️",
    ".exe": "💿",
    ".msi": "📦",
    ".py": "🐍",
    ".c": "💻",
    ".cpp": "💻",
    ".html": "🌐",
    ".css": "🎨",
    ".js": "📜",
    ".json": "🧩",
    ".csv": "📊",
}
    
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

def get_icon(path):
    if path.is_dir():
        return "📁"
    
    return FILE_ICONS.get(path.suffix.lower(), "📃")

def directory(drive):
    current = drive # Fetches the current directory
    while True:
        clear()
        title()
        print(f"{"\033[1;93m📂 CURRENT DIRECTORY:\033[0m\n":<10}{f"\033[1;97m{current}\033[0m"}")
        sleep(0.3)
        item_list = list(current.iterdir())

        visible_items= []
        folders= []
        files= []
        # To remove system folders and protected folders from the list
        for items in item_list:
            if items.is_dir() & should_skip(items):
                continue
            if items.is_dir():
                folders.append(items)
            if items.is_file():
                files.append(items)

        folders.sort(key= lambda x: x.name.lower())
        files.sort(key= lambda x: x.name.lower())
        visible_items = folders + files

        print("\n")
        print("\033[1;97m FOLDERS AND FILES\033[0m")
        print("\033[36m==========================================\033[0m")
        sleep(0.3)
        last_index = 0 
        for index, subitem in enumerate(visible_items, start=1):
            icon = get_icon(subitem)
            if subitem.is_dir():
                print(f"{" ":<3}{f"{index}.":<5}{f"{icon}":<3}{f"{subitem.name}"}")
                last_index = index
                sleep(0.1)
            else:
                size = subitem.stat().st_size
                formatted_size = format_size(size)
                print(f"{" ":<3}{f"{index}.":<5}{f"{icon}":<3}{f"{subitem.name}":<40}{f"{formatted_size}"}")
                sleep(0.1)
                
        if files:
            visible_items.append("🗃️   Organize Files")
            visible_items.append("🔁   Rename File")
            visible_items.append("🗑️   Delete File")

        if current != drive:
            visible_items.append("⬅️   Go Back")

        visible_items.append("⬅️   Back To Drive Menu")
        visible_items.append("❌  Exit")
        
        sleep(0.2)
        print("\n")
        print("\033[1;97m ACTIONS\033[0m")
        print("\033[36m==========================================\033[0m")
        for index, subitem in enumerate(visible_items[last_index:], start=last_index+1):         
            if not isinstance(subitem,(Path)) or not subitem.is_file():
                last_index = index
                print(f"{" ":<3}{f"{index}.":<5}{f"{subitem}"}")
                sleep(0.1)
        
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

        elif  "Go Back" in str(selected): # If go back is selected
            if current.parent != current:
                current = current.parent
            continue # This redraws the previous directory

        elif "Back To Drive Menu" in str(selected): # If go back is selected
            print(f"{" ":<12}{"\033[1;95mReturning to drive menu...\033[0m"}")
            sleep(0.5)
            return "Drive Menu"

        elif "Exit" in str(selected): # If a folder is selected 
            exit_app()

        
        
        