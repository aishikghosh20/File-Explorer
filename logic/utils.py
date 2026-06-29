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

    if choice == len(drives)+1:
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

DOCUMENTS = {
    ".txt", ".pdf", ".doc", ".docx",
    ".ppt", ".pptx", ".xls", ".xlsx"
}

IMAGES = {
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"
}

AUDIO = {
    ".mp3", ".wav", ".flac", ".aac"
}

VIDEOS = {
    ".mp4", ".mkv", ".avi", ".mov"
}

EXECUTABLES = {
    ".exe", ".msi"
}

ARCHIVES = {
    ".zip", ".rar", ".7z"
}

SUPPORTED_FILES = (
    DOCUMENTS |
    IMAGES |
    AUDIO |
    VIDEOS |
    EXECUTABLES |
    ARCHIVES
)
    
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

def open_file(file):
    try:
        print(f"{" ":<12}{"\033[1;95mOpening file...\033[0m"}")
        sleep(0.5)
        os.startfile(file)
    except OSError:
        print("\033[1;91mUnable to open this file\033[0m\n")
        sleep(1)      

def open_exe(file):
    try:
        print(f"{" ":<12}{"\033[1;95mOpening file...\033[0m"}")
        sleep(0.5)
        process = subprocess.Popen([str(file)])
        process.wait()
    except Exception:
        print("\033[1;91mUnable to open this file\033[0m\n")
        sleep(1)      

def choose_file(files):
    clear()
    print("\033[1;97mFILES LIST \033[0m")
    print("\033[36m==========================================\033[0m")
    last_index =0 
    for index, subitem in enumerate(files, start=1):
            icon = get_icon(subitem)
            last_index = index
            size = subitem.stat().st_size
            formatted_size = format_size(size)
            print(f"{" ":<3}{f"{index}.":<5}{f"{icon}":<3}{f"{subitem.name}":<40}{f"{formatted_size}"}")
    last_index+=1
    print(f"{" ":<3}{f"{last_index}.":<5}{f"❌":<3}Cancel")
            
    choice= 0
    # Prompt for user's choice
    valid = False
    while not(valid):
        try:
            choice = int(input("\033[1;93mSelect a file :\033[0m\n"))
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
        return None
        
    return files[choice-1]

def rename_file(file):
    
    INVALID_CHARS = '<>:"/|\\?*'
    # Prompt for the new name
    valid = False
    while not(valid):
        new_name = (input("\033[1;93mEnter the new name :\033[0m\n")).strip()
        # check for validity of the new name
        if (not new_name):
            print("\033[1;91mFilename cannot be empty\033[0m\n")
            continue
        elif (any(char in new_name for char in INVALID_CHARS)):
            print(f"\033[1;91m❌ Invalid filename\033[0m\n")
            sleep(0.5)
            continue

        new_path = file.with_name(new_name + file.suffix)

        if new_path.exists():
            print("\033[1;91m❌ A file with that name already exists\033[0m\n")
            sleep(0.5)
            continue

        try:
            file.rename(new_path)
            print(f"{" ":<12}{"\033[1;92m✅ FILE RENAMED SUCCESSFULLY\033[0m"}")
            sleep(0.5)
            print(f"\033[1;93m< OLD >\033[0m {file}  ⏩  {new_path} \033[1;93m< NEW >\033[0m")
            sleep(1.5)
            valid = True
            return new_path
        
        except FileExistsError:
            print(f"\033[1;91m❌ A file with that name already exists\033[0m\n")
            sleep(0.5)
        except PermissionError:
            print(f"\033[1;91m❌ Permission denied\033[0m\n")
            sleep(0.5)
        except OSError as e:
            print(f"\033[1;91m❌ {e}\033[0m\n")
            sleep(0.5)
    
def delete_file(file):
    clear()
    print("\033[1;91m⚠️ Are you sure about deleting:\033[0m")
    print(f"\033[1;97m{file}\033[0m\n")
    sleep(0.5)
    print("1. YES\n2. CANCEL")
    # Prompt for the user's choice
    valid = False
    while not(valid):
        try:
            choice = int(input("\033[1;93mChoose :\033[0m\n"))

        except ValueError:
            print("\033[1;91mENTER A VALID INPUT\033[0m\n")
            sleep(0.5)
            continue
        
        if choice == 1:
            try:
                file.unlink() # deletes this file
                print(f"{" ":<12}{"\033[1;92m✅ FILE DELETED SUCCESSFULLY\033[0m"}")
                sleep(0.5)
                return True

            except PermissionError:
                print(f"\033[1;91m❌ Permission denied\033[0m\n")
                sleep(0.5)

            except OSError as e:
                print(f"\033[1;91m❌ {e}\033[0m\n")
                sleep(0.5)
            
            return False
        
        elif choice == 2:
            return False
        
        else:
            print(f"\033[1;91mENTER A VALID OPTION\033[0m\n")
            sleep(0.5)
            



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
        last_index = 0 
        for index, subitem in enumerate(visible_items, start=1):
            icon = get_icon(subitem)
            if subitem.is_dir():
                print(f"{" ":<3}{f"{index}.":<5}{f"{icon}":<3}{f"{subitem.name}"}")
                last_index = index
                
            else:
                size = subitem.stat().st_size
                formatted_size = format_size(size)
                print(f"{" ":<3}{f"{index}.":<5}{f"{icon}":<3}{f"{subitem.name}":<40}{f"{formatted_size}"}")
                
                
        if len(files) > 1:
            visible_items.append("🗃️   Organize Files")
            visible_items.append("🔁  Rename File")
            visible_items.append("🗑️   Delete File")
        if len(folders) > 1:
            visible_items.append("🔁  Rename Folder")
            visible_items.append("🗑️   Delete Folder")

        if current != drive:
            visible_items.append("⬅️   Go Back")

        visible_items.append("⬅️   Back To Drive Menu")
        visible_items.append("❌  Exit")
        
        print("\n")
        print("\033[1;97m ACTIONS\033[0m")
        print("\033[36m==========================================\033[0m")
        for index, subitem in enumerate(visible_items[last_index:], start=last_index+1):         
            if not isinstance(subitem,(Path)) or not subitem.is_file():
                last_index = index
                print(f"{" ":<3}{f"{index}.":<5}{f"{subitem}"}")
                # sleep(0.1)
        
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
        
        if isinstance(selected, Path): # If a folder is opened
            if selected.is_dir():
                current = selected
                continue
            elif selected.is_file(): # To open and run selected file
                extension = selected.suffix.lower()
                if extension in SUPPORTED_FILES: # To check the supportability of the file
                    if ".exe" in extension: # To prevent accidental execution of file
                        clear()
                        print("\033[1;93m⚠️ You're about to run:\033[0m")
                        print(f"\033[1;97m{selected}\033[0m\n")
                        sleep(0.5)
                        print("1. Run\n2. Cancel")
                        # Prompt for user's choice
                        run_check =0
                        valid = False
                        while not(valid):
                            try:
                                run_check = int(input("\033[1;93mChoose :\033[0m\n"))
                            except ValueError:
                                print("\033[1;91mENTER A VALID INPUT\033[0m\n")
                                sleep(0.5)
                                continue
                            if (1<=run_check<=2):
                                valid = True
                            else:
                                print(f"\033[1;91mENTER A VALID OPTION INPUT\033[0m\n")
                                sleep(0.5)
                        
                        if run_check == 1:
                            open_exe(selected)  
                            continue 
                        else : 
                            continue # This redraws the previous directory

                    open_file(selected)  
                    continue 
        
                else:
                    print("\033[1;91m❌ This file type is not supported\033[0m\n")
                    sleep(0.7)

        elif  "Go Back" in str(selected): # If go back is selected
            if current.parent != current:
                current = current.parent
            continue # This redraws the previous directory

        elif "Back To Drive Menu" in str(selected): # If go back is selected
            print(f"{" ":<12}{"\033[1;95mReturning to drive menu...\033[0m"}")
            sleep(0.5)
            return "Drive Menu"

        elif "Exit" in str(selected): 
            exit_app()

        elif "Rename File" in str(selected):
            file = choose_file(files) # For user to choose a file
            if file is None:
                continue # redraws the directory menu 

            while True:
                clear()
                print("\033[1;93mSelected File:\033[0m")
                print(f"\033[1;97m{file}\033[0m\n")
                sleep(0.5)
                print("1.✅  Rename this file")
                print("2.⬅️   Choose another file")
                print("3.❌ Cancel")

                try:
                    choice = int(input("\033[1;93mChoose :\033[0m\n"))
                except ValueError:
                    print("\033[1;91mENTER A VALID INPUT\033[0m\n")
                    sleep(0.5)
                    continue

                if choice == 1:
                    file = rename_file(file)
                    sleep(0.5)
                    break # Leave the rename menu

                elif choice == 2:
                    file = choose_file(files) # select another file

                elif choice == 3:
                   break

                else:
                    print("\033[1;91mENTER A VALID OPTION\033[0m\n")
                    sleep(0.5)
                    continue
                    
        elif "Delete File" in str(selected):
            file = choose_file(files) # For user to choose a file
            if file is None:
                continue # redraws the directory menu 

            while True:
                clear()
                print("\033[1;93mSelected File:\033[0m")
                print(f"\033[1;97m{file}\033[0m\n")
                sleep(0.5)
                print("1.✅  Delete this file")
                print("2.⬅️   Choose another file")
                print("3.❌ Cancel")

                try:
                    choice = int(input("\033[1;93mChoose :\033[0m\n"))
                except ValueError:
                    print("\033[1;91mENTER A VALID INPUT\033[0m\n")
                    sleep(0.5)
                    continue

                if choice == 1:
                    if(delete_file(file)):
                        sleep(0.5)
                        break # Leave the rename menu
                    else:
                        continue # Stay in the delete menu

                elif choice == 2:
                    file = choose_file(files) # select another file

                elif choice == 3:
                   break

                else:
                    print("\033[1;91mENTER A VALID OPTION\033[0m\n")
                    sleep(0.5)
                    continue
        
        