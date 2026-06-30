from time import sleep
from pathlib import Path
from .folder_check import should_skip
import os, subprocess, shutil
from send2trash import send2trash
from reportlab.pdfgen import canvas
from docx import Document
from openpyxl import Workbook
from pptx import Presentation
import zipfile

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

def choose_folder(folder):
    clear()
    print("\033[1;97mFOLDER LIST \033[0m")
    print("\033[36m==========================================\033[0m")
    last_index =0 
    for index, subitem in enumerate(folder, start=1):
            icon = get_icon(subitem)
            print(f"{" ":<3}{f"{index}.":<5}{f"{icon}":<3}{f"{subitem.name}"}")
            last_index = index
    last_index+=1
    print(f"{" ":<3}{f"{last_index}.":<5}{f"❌":<3}Cancel")
            
    choice= 0
    # Prompt for user's choice
    valid = False
    while not(valid):
        try:
            choice = int(input("\033[1;93mSelect a folder :\033[0m\n"))
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
        
    return folder[choice-1]

def rename_folder(folder):
    INVALID_CHARS = '<>:"/|\\?*'
    # Prompt for the new name
    valid = False
    while not(valid):
        new_name = (input("\033[1;93mEnter the new name :\033[0m\n")).strip()
        # check for validity of the new name
        if (not new_name):
            print("\033[1;91mFoldername cannot be empty\033[0m\n")
            sleep(0.5)
            continue
        elif (any(char in new_name for char in INVALID_CHARS)):
            print(f"\033[1;91m❌ Invalid foldername\033[0m\n")
            sleep(0.5)
            continue

        new_path = folder.with_name(new_name)

        if new_path.exists():
            print("\033[1;91m❌ A folder with that name already exists\033[0m\n")
            sleep(0.5)
            continue

        try:
            folder.rename(new_path)
            print(f"{" ":<12}{"\033[1;92m✅ FOLDER RENAMED SUCCESSFULLY\033[0m"}")
            sleep(0.5)
            print(f"\033[1;93m< OLD >\033[0m {folder}  ⏩  {new_path} \033[1;93m< NEW >\033[0m")
            sleep(1.5)
            valid = True
            return new_path
        
        except FileExistsError:
            print(f"\033[1;91m❌ A folder with that name already exists\033[0m\n")
            sleep(0.5)
        except PermissionError:
            print(f"\033[1;91m❌ Permission denied\033[0m\n")
            sleep(0.5)
        except OSError as e:
            print(f"\033[1;91m❌ {e}\033[0m\n")
            sleep(0.5)

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
                send2trash(file) # deletes this file
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
            
def delete_folder(folder):
    clear()
    print("\033[1;91m⚠️ Are you sure about deleting:\033[0m")
    print(f"\033[1;97m{folder}\033[0m\n")
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
                send2trash(folder) # deletes this file
                print(f"{" ":<12}{"\033[1;92m✅ FOLDER DELETED SUCCESSFULLY\033[0m"}")
                sleep(0.5)
                return True

            except PermissionError:
                print(f"\033[1;91m❌ Permission denied\033[0m\n")
                sleep(0.5)

            except OSError:
                if any(folder.iterdir()):
                    print("\n\033[1;91m⚠️ Are you sure about deleting:\033[0m")
                    print(f"\033[1;97m{folder}\033[0m\n")
                    print("\033[1;93mDeleting it will permanently remove:\033[0m")
                    print(f"\033[1;97m• All Files\n• All Folders\033[0m\n")
                    sleep(0.5)
                    print("1. DELETE EVERYTHING\n2. CANCEL")

                    # Prompt for the choice
                    check = False
                    while not(check):
                        try:
                            choice = int(input("\033[1;93mChoose :\033[0m\n"))

                        except ValueError:
                            print("\033[1;91mENTER A VALID INPUT\033[0m\n")
                            sleep(0.5)
                            continue

                        if choice == 1:
                            try:
                                shutil.rmtree(folder)
                                print(f"{" ":<12}{"\033[1;92m✅ FOLDER DELETED SUCCESSFULLY\033[0m"}")
                                sleep(0.5)
                                return True
                        
                            except PermissionError:
                                print(f"\033[1;91m❌ Permission denied\033[0m\n")
                                sleep(0.5)

                            except OSError as e:
                                print(f"\033[1;91m❌ {e}\033[0m\n")
                                sleep(0.5)

                        return False
                    
            return False
        
        elif choice == 2:
            return False
        
        else:
            print(f"\033[1;91mENTER A VALID OPTION\033[0m\n")
            sleep(0.5)

def select_destination(file):
    current = file.parent
    start_drive = Path(file.anchor)

    while True:
        clear()
        title()

        print("\033[1;93m📁 SELECT DESTINATION\033[0m\n")

        print("\033[1;96mSelected File:\033[0m")
        print(f"\033[1;97m{file}\033[0m\n")

        print("\033[1;96mCurrent Folder:\033[0m")
        print(f"\033[1;97m{current}\033[0m\n")

        sleep(0.3)

        folders = []

        try:
            for item in current.iterdir():
                if item.is_dir() and not should_skip(item):
                    folders.append(item)

        except PermissionError:
            print("\033[1;91mPermission Denied\033[0m")
            sleep(0.8)
            current = current.parent
            continue

        folders.sort(key=lambda x: x.name.lower())

        if not folders:
            print("\033[1;90m(No subfolders found)\033[0m\n")

        last_index = 0

        for index, folder in enumerate(folders, start=1):
            print(f"{index}. 📁 {folder.name}")
            last_index = index

        print()

        print(f"{last_index+1}. 📋 Copy Here")

        if current != start_drive:
            print(f"{last_index+2}. ⬅ Go Back")
            print(f"{last_index+3}. 🖥 Change Drive")
            print(f"{last_index+4}. ❌ Cancel")
        else:
            print(f"{last_index+2}. 🖥 Change Drive")
            print(f"{last_index+3}. ❌ Cancel")

        while True:
            try:
                choice = int(input("\n\033[1;93mChoose : \033[0m"))
                break

            except ValueError:
                print("\033[1;91mENTER A VALID INPUT\033[0m")
                sleep(0.5)

        # Open folder
        if 1 <= choice <= last_index:
            current = folders[choice - 1]
            continue

        # Copy here
        if choice == last_index + 1:
            return current

        if current != start_drive:

            # Go back
            if choice == last_index + 2:
                current = current.parent
                continue

            # Change drive
            elif choice == last_index + 3:
                drive = main_drives()

                if drive is not None:
                    current = drive
                    start_drive = drive

                continue

            # Cancel
            elif choice == last_index + 4:
                return None

        else:

            # Change drive
            if choice == last_index + 2:
                drive = main_drives()

                if drive is not None:
                    current = drive
                    start_drive = drive

                continue

            # Cancel
            elif choice == last_index + 3:
                return None

        print("\033[1;91mENTER A VALID OPTION\033[0m")
        sleep(0.5)

def copy_file(file):
    clear()
    destination = select_destination(file)
    if destination is None:
        return False

    new_path = destination / file.name

    # If the file already exists- create a duplicate 
    if new_path.exists():
        stem = file.stem #filename without the extension
        suffix = file.suffix # extension

        counter =1

        while True: # To increase the counter appropriately
            new_path = destination/f"{stem}({counter}){suffix}"
            if not new_path.exists(): # if a duplicate doesn't exist
                break
            counter +=1

    # To copy and paste the file
    try:
        shutil.copy2(file, new_path)

        print("\n\033[1;92m✅ FILE COPIED SUCCESSFULLY\033[0m")
        print(f"\n\033[1;93mFROM >\033[0m {file}")
        print(f"\033[1;93mTO   >\033[0m {new_path}")

        sleep(1.5)
        return new_path

    except shutil.SameFileError:
        print("\033[1;91m⚠️ File already exists in this location\033[0m")
        
    except PermissionError:
        print("\033[1;91m❌ Permission denied\033[0m")
        sleep(0.5)

    except OSError as e:
        print(f"\033[1;91m❌ {e}\033[0m")
        sleep(0.5)

    return None

def copy_folder(folder):
    clear()
    destination = select_destination(folder)
    if destination is None:
        return False

    new_path = destination / folder.name

    # If the file already exists- create a duplicate 
    if new_path.exists():
        name = folder.name

        counter =1

        while True: # To increase the counter appropriately
            new_path = destination/f"{name} ({counter})"
            if not new_path.exists(): # if a duplicate doesn't exist
                break
            counter +=1

    # To copy and paste the file
    try:
        shutil.copytree(folder, new_path)

        print("\n\033[1;92m✅ FOLDER COPIED SUCCESSFULLY\033[0m")
        print(f"\n\033[1;93mFROM >\033[0m {folder}")
        print(f"\033[1;93mTO   >\033[0m {new_path}")

        sleep(1.5)
        return new_path
   
    except PermissionError:
        print("\033[1;91m❌ Permission denied\033[0m")
        sleep(0.5)

    except OSError as e:
        print(f"\033[1;91m❌ {e}\033[0m")
        sleep(0.5)

    return None

def move_file(file):
    clear()
    destination = select_destination(file.parent)
    if destination is None:
        return False

    new_path = destination / file.name

    # If the file already exists- create a duplicate 
    if new_path.exists():
        stem = file.stem #filename without the extension
        suffix = file.suffix # extension

        counter =1

        while True: # To increase the counter appropriately
            new_path = destination/f"{stem}({counter}){suffix}"
            if not new_path.exists(): # if a duplicate doesn't exist
                break
            counter +=1

    # To copy and paste the file
    try:
        shutil.move(file, new_path)

        print("\n\033[1;92m✅ FILE MOVIED SUCCESSFULLY\033[0m")
        print(f"\n\033[1;93mFROM >\033[0m {file}")
        print(f"\033[1;93mTO   >\033[0m {new_path}")

        sleep(1.5)
        return new_path
        
    except PermissionError:
        print("\033[1;91m❌ Permission denied\033[0m")
        sleep(0.5)

    except OSError as e:
        print(f"\033[1;91m❌ {e}\033[0m")
        sleep(0.5)

    return None

def move_folder(folder):
    clear()
    destination = select_destination(folder.parent)
    if destination is None:
        return False

    new_path = destination / folder.name

    # If the file already exists- create a duplicate 
    if new_path.exists():
        name = folder.name

        counter =1

        while True: # To increase the counter appropriately
            new_path = destination/f"{name} ({counter})"
            if not new_path.exists(): # if a duplicate doesn't exist
                break
            counter +=1

    # To copy and paste the file
    try:
        shutil.move(folder, new_path)

        print("\n\033[1;92m✅ FOLDER MOVIED SUCCESSFULLY\033[0m")
        print(f"\n\033[1;93mFROM >\033[0m {folder}")
        print(f"\033[1;93mTO   >\033[0m {new_path}")
        sleep(1.5)
        return new_path
        
    except PermissionError:
        print("\033[1;91m❌ Permission denied\033[0m")
        sleep(0.5)

    except OSError as e:
        print(f"\033[1;91m❌ {e}\033[0m")
        sleep(0.5)

    return None

def create_folder(current):
    clear()
    print("\033[1;97mCREATE FOLDER\033[0m")
    print("\033[36m==========================================\033[0m")
        
    INVALID_CHARS = '<>:"/|\\?*'
    # Prompt for the new name
    while True:
        folder_name = input("\n\033[1;93mEnter the folder name\n\033[0m").strip()
        if (not folder_name):
            print("\033[1;91mContinuing with default name\033[0m\n")
            folder_name = "New_folder"
            sleep(1)

        elif (any(char in folder_name for char in INVALID_CHARS)):
            print(f"\033[1;91m❌ Invalid foldername\033[0m\n")
            sleep(0.5)
            continue

        new_folder = current / folder_name

        if new_folder.exists():
            print("\033[1;91m❌ A folder with that name already exists\033[0m\n")
            sleep(0.5)
            continue

        try:
            new_folder.mkdir()
            print(f"{" ":<12}{"\033[1;92m✅ FOLDER CREATED SUCCESSFULLY\033[0m"}")
            sleep(1)
            return new_folder
        
        except PermissionError:
            print(f"\033[1;91m❌ Permission denied\033[0m\n")
            sleep(0.5)

        except OSError as e:
            print(f"\033[1;91m❌ {e}\033[0m\n")
            sleep(0.5)

def create_file(current):
        
    INVALID_CHARS = '<>:"/|\\?*'
    # Prompt for the new name
    while True:
        clear()
        print("\033[1;97mCREATE FILE\033[0m")
        print("\033[36m==========================================\033[0m")
        print("\033[1;93m📜 SELECT FILE-TYPE\033[0m\n")
        print("\033[1;97m1.📝 Text Document\n2.📝 PDF Document\n3.📰 Microsoft Word Document\n4.📊 Microsoft Excel Worksheet\n5.🎥 Microsoft Powerpoint Presentation\n6.❌ Cancel\n\033[0m\n")
        
        try:
            choice = int(input("\033[1;93mChoose :\033[0m\n"))
        except ValueError:
                print("\033[1;91mENTER A VALID INPUT\033[0m\n")
                sleep(0.5)
                continue
        if not(1<=choice<=6):
            print(f"\033[1;91mENTER A VALID BETWEEN 1 AND 6033[0m\n")
            sleep(0.5)
            continue

        if choice ==  6:
            return None

        file_name = input("\n\033[1;93mEnter the file name\n\033[0m").strip().strip(".").strip('"').strip("'")
        if (not file_name):
            print("\033[1;91mFilename cannot be empty\033[0m\n")
            sleep(0.5)
            continue
        elif (any(char in file_name for char in INVALID_CHARS)):
            print(f"\033[1;91m❌ Invalid filename\033[0m\n")
            sleep(0.5)
            continue

        if choice ==1:
            file_name += ".txt"
            new_file = current / file_name

            if new_file.exists():
                print("\033[1;91m❌ A file with that name already exists\033[0m\n")
                sleep(0.5)
                continue

            try:
                new_file.touch()
                print(f"{" ":<12}{"\033[1;92m✅ FILE CREATED SUCCESSFULLY\033[0m"}")
                sleep(1)
                return new_file
            
            except PermissionError:
                print(f"\033[1;91m❌ Permission denied\033[0m\n")
                sleep(0.5)

            except OSError as e:
                print(f"\033[1;91m❌ {e}\033[0m\n")
                sleep(0.5)

        elif choice ==2:
            # TO create a valid empty pdf document
            file_name += ".pdf"
            new_file = current / file_name

            if new_file.exists():
                print("\033[1;91m❌ A file with that name already exists\033[0m\n")
                sleep(0.5)
                continue

            try:
                c= canvas.Canvas(str(new_file))
                c.save()
                print(f"{" ":<12}{"\033[1;92m✅ PDF CREATED SUCCESSFULLY\033[0m"}")
                sleep(1)
                return new_file
            
            except PermissionError:
                print(f"\033[1;91m❌ Permission denied\033[0m\n")
                sleep(0.5)

            except OSError as e:
                print(f"\033[1;91m❌ {e}\033[0m\n")
                sleep(0.5)


        elif choice ==3:
            # TO create a valid empty word document
            file_name += ".docx"
            new_file = current / file_name

            if new_file.exists():
                print("\033[1;91m❌ A file with that name already exists\033[0m\n")
                sleep(0.5)
                continue

            try:
                doc= Document()
                doc.save(str(new_file))
                print(f"{" ":<12}{"\033[1;92m✅ WORD DOCUMENT CREATED SUCCESSFULLY\033[0m"}")
                sleep(1)
                return new_file
            
            except PermissionError:
                print(f"\033[1;91m❌ Permission denied\033[0m\n")
                sleep(0.5)

            except OSError as e:
                print(f"\033[1;91m❌ {e}\033[0m\n")
                sleep(0.5)

        elif choice ==4:
            # TO create a valid empty excel worksheet
            file_name += ".xlsx"
            new_file = current / file_name

            if new_file.exists():
                print("\033[1;91m❌ A file with that name already exists\033[0m\n")
                sleep(0.5)
                continue

            try:
                wb= Workbook()
                wb.save(str(new_file))
                print(f"{" ":<12}{"\033[1;92m✅ EXCEL WORKSHEET CREATED SUCCESSFULLY\033[0m"}")
                sleep(1)
                return new_file
            
            except PermissionError:
                print(f"\033[1;91m❌ Permission denied\033[0m\n")
                sleep(0.5)

            except OSError as e:
                print(f"\033[1;91m❌ {e}\033[0m\n")
                sleep(0.5)

        elif choice ==5:
            # TO create a valid empty powerpoint presentation
            file_name += ".pptx"
            new_file = current / file_name

            if new_file.exists():
                print("\033[1;91m❌ A file with that name already exists\033[0m\n")
                sleep(0.5)
                continue

            try:
                ppt= Presentation()
                ppt.save(str(new_file))
                print(f"{" ":<12}{"\033[1;92m✅ PDF CREATED SUCCESSFULLY\033[0m"}")
                sleep(1)
                return new_file
            
            except PermissionError:
                print(f"\033[1;91m❌ Permission denied\033[0m\n")
                sleep(0.5)

            except OSError as e:
                print(f"\033[1;91m❌ {e}\033[0m\n")
                sleep(0.5)



