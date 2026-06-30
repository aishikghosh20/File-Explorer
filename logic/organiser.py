import os, sys
from pathlib import Path
from time import sleep,perf_counter
import shutil
from .folder_check import should_skip
from .utils import clear


def organize(current):
    clear()
    print("\033[1;97mORGANIZE FILES\033[0m")
    print("\033[36m==========================================\033[0m")

    # Creating database folder category extensions
    IMAGES = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}

    VIDEOS = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"}

    AUDIO = {".mp3", ".wav", ".aac", ".flac", ".ogg"}

    DOCUMENTS = {
        ".txt",
        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx"
    }

    ARCHIVES = {
        ".zip",
        ".rar",
        ".7z",
        ".tar",
        ".gz"
    }

    # Creating categories dictionary
    IMAGE_FOLDER_NAMES = {"images", "image", "photo", "photos", "pic", "pics", "pictures"}
    VIDEO_FOLDER_NAMES = {"videos", "video", "movies", "movie","vid", "vids", "film", "films", "clips", "clip"}
    AUDIO_FOLDER_NAMES = {"audio", "audios", "music", "songs","song"}
    DOCUMENT_FOLDER_NAMES = {"docs", "document", "documents", "files", "pdfs"}
    ARCHIVE_FOLDER_NAMES = {"archive", "archives", "archs", "zips", "compressed"}

    CATEGORY_ALIASES = {
        "Images" : IMAGE_FOLDER_NAMES,
        "Videos" : VIDEO_FOLDER_NAMES,
        "Audio" : AUDIO_FOLDER_NAMES,
        "Documents" : DOCUMENT_FOLDER_NAMES,
        "Archives" : ARCHIVE_FOLDER_NAMES
    }

    CATEGORY_EXTENSIONS = {
        "Images" : IMAGES,
        "Videos" : VIDEOS,
        "Audio" : AUDIO,
        "Documents" : DOCUMENTS,
        "Archives" : ARCHIVES
    }
    
    # To scan the items in the current directory
    print(f"{"\033[1;93m📂 CURRENT DIRECTORY:\033[0m\n":<10}{f"\033[1;97m{current}\033[0m"}")
    print("\033[36m==========================================\033[0m\n")
    sleep(0.5)
    start = perf_counter()
    print("\033[1;93m📂 Scanning current directory...\033[0m")  
    sleep(1)

    existing_folder = {}
    for folder in current.iterdir():
        if not folder.is_dir():
            continue

        if (should_skip(folder)):
            continue

        if folder.is_dir():
            existing_folder[folder.name.lower()] = folder


    # Creating folders or using existing folders as destinations
    destinations = {}
    existing_count = 0
    created_count = 0 

    for category, extension in CATEGORY_EXTENSIONS.items(): # To get the extensions of that category
        matched = False

        for file in current.iterdir():
            if not file.is_file():
                continue

            # to check if a file exists with such extensions
            if file.suffix.lower() in extension:
                matched = True
                break

        if not matched: # To prevent creating unnecessary folders
            continue

        # To check if a folder already exists
        folder_found = None
        for alias in CATEGORY_ALIASES[category]:
            if alias in existing_folder:
                folder_found = existing_folder[alias]
                break
        
        if folder_found:
            destinations[category] = folder_found
            existing_count += 1
            print(f"\033[1;97m✅ Using existing folder: \033[0m{folder_found.name}")
            sleep(0.2)

        else: # create a new folder for that category as a new destination
            new_folder = current / category
            new_folder.mkdir()
            destinations[category] = new_folder
            created_count += 1
            print(f"\033[1;97m📁 Created folder: \033[0m{category}")
            sleep(0.2)


    category_count = len(destinations)
    sleep(0.5)
    if category_count == 0:
        print("\033[1;93m⚠️ No supported files found to organize")
        sleep(1)
        return
    print(f"\033[1;97m✅ {category_count} categor{"y" if category_count == 1 else "ies"} detected.\033[0m")
    sleep(0.5)

    print("\n\033[1;93m📦 Organizing files...\033[0m")
    sleep(0.5)

    # Moving files in their appropriate folder
    moved = 0
    duplicates = 0
    skipped = 0
    for file in current.iterdir():
        if file.is_dir():
            if (should_skip(file)):
                print(f"\033[1;93m⏭️  Skipping {file.name} (System Folder)\033[0m\n")
                skipped += 1
                sleep(0.1)
                continue

        if not file.is_file():
            continue

        matched = False # Reset for each file

        # To loop through the categories
        for category,extension in CATEGORY_EXTENSIONS.items():
            if file.suffix.lower() in extension:
                matched = True
                destination = destinations[category]
                new_path = destination / file.name

               # If the file already exists- create a duplicate 
                if new_path.exists():
                    stem = file.stem #filename without the extension
                    suffix = file.suffix # extension

                    counter =1
                    duplicates += 1

                    while True: # To increase the counter appropriately
                        new_path = destination/f"{stem}({counter}){suffix}"
                        if not new_path.exists(): # if a duplicate doesn't exist
                            break
                        counter +=1

                    print("\033[1;97m⚠️ Duplicate detected...")
                    print(f"{file.name}  →  renamed to {new_path.name}")
                    sleep(0.1)

                if file.parent == destination: # TO prevent moving the file to the folder it's already in
                    skipped += 1
                    print(f"⏭️  Skipping {file.name} as it is already in {destination.name}\n")
                    sleep(0.1)
                    break

                # To copy and paste the file
                try:
                    shutil.move(file, new_path)
                    moved += 1
                    print(f"▶️  {file.name}  →  {destination.name}\n" )
                    sleep(0.1)
                    break # To leave the category loop after the file has been moved

                except shutil.SameFileError:
                    print("\033[1;91m⚠️ File already exists in this location\033[0m")
                    sleep(0.5)
        
            
                except PermissionError:
                    print("\033[1;91m❌ Permission denied\033[0m")
                    sleep(0.5)

                except OSError as e:
                    print(f"\033[1;91m❌ {e}\033[0m")
                    sleep(0.5)

        # Runs only if no category matched
        if not matched:
            skipped += 1
            print(f"\033[1;93m⏭️  Skipping {file.name} (Unsupported File)\033[0m\n")
            sleep(0.1)


    end = perf_counter()
    sleep(0.5)
    print("\n")
    print("\033[1;96m" + "─" * 35 + "\033[0m")
    print("\033[1;92m      ✅ ORGANIZATION COMPLETE\033[0m")
    print("\033[1;96m" + "─" * 35 + "\033[0m")
    sleep(0.5)
    print(f"\033[1;97m📂 Categories Detected : {category_count}\033[0m")
    print(f"\033[1;97m📄 Files Moved         : {moved}\033[0m")
    print(f"\033[1;97m📁 Folders Created     : {created_count}\033[0m")
    print(f"\033[1;97m📂 Existing Folders    : {existing_count}\033[0m")

    if skipped > 0:
        print(f"\033[1;93m⏭️ Files Skipped       : {skipped}\033[0m")

    if duplicates > 0:
        print(f"\033[1;93m✔️ Duplicates Fixed    : {duplicates}\033[0m")

    print(f"\033[1;97m⏱️ Time Taken          : {end - start:.2f} sec\033[0m")

    print("\033[1;96m" + "─" * 35 + "\033[0m")

    input("\n\033[1;93mPress Enter to continue...\033[0m")

