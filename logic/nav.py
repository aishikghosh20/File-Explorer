from . import utils 
from .folder_check import should_skip
from pathlib import Path
from .organiser import organize

def directory(drive):
    current = drive # Fetches the current directory
    while True:
        utils.clear()
        utils.title()
        print(f"{"\033[1;93m📂 CURRENT DIRECTORY:\033[0m\n":<10}{f"\033[1;97m{current}\033[0m"}")
        utils.sleep(0.3)
        item_list = list(current.iterdir())

        extensions_list = set()
        for items in current.iterdir():
            if items.is_file() and items.suffix:
                extensions_list.add(items.suffix.lower())

        visible_items= []
        folders= []
        files= []
        # To remove system folders and protected folders from the list
        for items in item_list:
            if items.is_dir() and should_skip(items):
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
            icon = utils.get_icon(subitem)
            if subitem.is_dir():
                print(f"{" ":<3}{f"{index}.":<5}{f"{icon}":<3}{f"{subitem.name}"}")
                last_index = index
                
            else:
                size = subitem.stat().st_size
                formatted_size = utils.format_size(size)
                print(f"{" ":<3}{f"{index}.":<5}{f"{icon}":<3}{f"{subitem.name}":<40}{f"{formatted_size}"}")
                
                
        if len(extensions_list) >=2:
            visible_items.append("🗃️   Organize Files")

        if len(files) > 1:
            visible_items.append("🔁  Rename File")
            visible_items.append("🗑️   Delete File")
            visible_items.append("⤴️   Copy File")
            visible_items.append("🚚  Move File")
            
        if len(folders) > 1:
            visible_items.append("🔁  Rename Folder")
            visible_items.append("🗑️   Delete Folder")
            visible_items.append("⤴️   Copy Folder")
            visible_items.append("🚚  Move Folder")

        visible_items.append("📂  Create Folder")
        visible_items.append("📜  Create File")
        
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
                utils.sleep(0.5)
                continue
            if (1<=choice<=last_index):
                valid = True
            else:
                print(f"\033[1;91mENTER A VALID BETWEEN 1 AND {last_index}\033[0m\n")
                utils.sleep(0.5)

        selected = visible_items[choice-1]
        
        if isinstance(selected, Path): # If a folder is opened
            if selected.is_dir():
                current = selected
                continue
            elif selected.is_file(): # To open and run selected file
                extension = selected.suffix.lower()
                if extension in utils.SUPPORTED_FILES: # To check the supportability of the file
                    if ".exe" in extension: # To prevent accidental execution of file
                        utils.clear()
                        print("\033[1;93m⚠️ You're about to run:\033[0m")
                        print(f"\033[1;97m{selected}\033[0m\n")
                        utils.sleep(0.5)
                        print("1. Run\n2. Cancel")
                        # Prompt for user's choice
                        run_check =0
                        valid = False
                        while not(valid):
                            try:
                                run_check = int(input("\033[1;93mChoose :\033[0m\n"))
                            except ValueError:
                                print("\033[1;91mENTER A VALID INPUT\033[0m\n")
                                utils.sleep(0.5)
                                continue
                            if (1<=run_check<=2):
                                valid = True
                            else:
                                print(f"\033[1;91mENTER A VALID OPTION INPUT\033[0m\n")
                                utils.sleep(0.5)
                        
                        if run_check == 1:
                            utils.open_exe(selected)  
                            continue 
                        else : 
                            continue # This redraws the previous directory

                    utils.open_file(selected)  
                    continue 
        
                else:
                    print("\033[1;91m❌ This file type is not supported\033[0m\n")
                    utils.sleep(0.7)

        elif  "Go Back" in str(selected): # If go back is selected
            if current.parent != current:
                current = current.parent
            continue # This redraws the previous directory

        elif "Back To Drive Menu" in str(selected): # If go back is selected
            print(f"{" ":<12}{"\033[1;95mReturning to drive menu...\033[0m"}")
            utils.sleep(0.5)
            return "Drive Menu"

        elif "Exit" in str(selected): 
            utils.exit_app()

        elif "Rename File" in str(selected):
            file = utils.choose_file(files) # For user to choose a file
            if file is None:
                continue # redraws the directory menu 

            while True:
                utils.clear()
                print("\033[1;93mSelected File:\033[0m")
                print(f"\033[1;97m{file}\033[0m\n")
                utils.sleep(0.5)
                print("1.✅  Rename this file")
                print("2.⬅️   Choose another file")
                print("3.❌ Cancel")

                try:
                    choice = int(input("\033[1;93mChoose :\033[0m\n"))
                except ValueError:
                    print("\033[1;91mENTER A VALID INPUT\033[0m\n")
                    utils.sleep(0.5)
                    continue

                if choice == 1:
                    file = utils.rename_file(file)
                    utils.sleep(0.5)
                    break # Leave the rename menu

                elif choice == 2:
                    file = utils.choose_file(files) # select another file

                elif choice == 3:
                   break

                else:
                    print("\033[1;91mENTER A VALID OPTION\033[0m\n")
                    utils.sleep(0.5)
                    continue
                    
        elif "Rename Folder" in str(selected):
            folder = utils.choose_folder(folders) # For user to choose a file
            if folder is None:
                continue # redraws the directory menu 

            while True:
                utils.clear()
                print("\033[1;93mSelected Folder:\033[0m")
                print(f"\033[1;97m{folder}\033[0m\n")
                utils.sleep(0.5)
                print("1.✅  Rename this folder")
                print("2.⬅️   Choose another folder")
                print("3.❌ Cancel")

                try:
                    choice = int(input("\033[1;93mChoose :\033[0m\n"))
                except ValueError:
                    print("\033[1;91mENTER A VALID INPUT\033[0m\n")
                    utils.sleep(0.5)
                    continue

                if choice == 1:
                    folder = utils.rename_folder(file)
                    utils.sleep(0.5)
                    break # Leave the rename menu

                elif choice == 2:
                    folder = utils.choose_folder(folders) # select another file

                elif choice == 3:
                   break

                else:
                    print("\033[1;91mENTER A VALID OPTION\033[0m\n")
                    utils.sleep(0.5)
                    continue

        elif "Delete File" in str(selected):
            file = utils.choose_file(files) # For user to choose a file
            if file is None:
                continue # redraws the directory menu 

            while True:
                utils.clear()
                print("\033[1;93mSelected File:\033[0m")
                print(f"\033[1;97m{file}\033[0m\n")
                utils.sleep(0.5)
                print("1.✅  Delete this file")
                print("2.⬅️   Choose another file")
                print("3.❌ Cancel")

                try:
                    choice = int(input("\033[1;93mChoose :\033[0m\n"))
                except ValueError:
                    print("\033[1;91mENTER A VALID INPUT\033[0m\n")
                    utils.sleep(0.5)
                    continue

                if choice == 1:
                    if(utils.delete_file(file)):
                        utils.sleep(0.5)
                        break # Leave the rename menu
                    else:
                        continue # Stay in the delete menu

                elif choice == 2:
                    file = utils.choose_file(files) # select another file

                elif choice == 3:
                   break

                else:
                    print("\033[1;91mENTER A VALID OPTION\033[0m\n")
                    utils.sleep(0.5)
                    continue
        
        elif "Delete Folder" in str(selected):
            folder = utils.choose_folder(folders) # For user to choose a file
            if folder is None:
                continue # redraws the directory menu 

            while True:
                utils.clear()
                print("\033[1;93mSelected File:\033[0m")
                print(f"\033[1;97m{folder}\033[0m\n")
                utils.sleep(0.5)
                print("1.✅  Delete this folder")
                print("2.⬅️   Choose another folder")
                print("3.❌ Cancel")

                try:
                    choice = int(input("\033[1;93mChoose :\033[0m\n"))
                except ValueError:
                    print("\033[1;91mENTER A VALID INPUT\033[0m\n")
                    utils.sleep(0.5)
                    continue

                if choice == 1:
                    if(utils.delete_folder(folder)):
                        utils.sleep(0.5)
                        break # Leave the rename menu
                    else:
                        continue # Stay in the delete menu

                elif choice == 2:
                    file = utils.choose_folder(folders) # select another file

                elif choice == 3:
                   break

                else:
                    print("\033[1;91mENTER A VALID OPTION\033[0m\n")
                    utils.sleep(0.5)
                    continue
        
        elif "Copy File" in str(selected):
            file = utils.choose_file(files) # For user to choose a file
            if file is None:
                continue # redraws the directory menu 

            while True:
                utils.clear()
                print("\033[1;93mSelected File:\033[0m")
                print(f"\033[1;97m{file}\033[0m\n")
                utils.sleep(0.5)
                print("1.✅  Copy this file")
                print("2.⬅️   Choose another file")
                print("3.❌ Cancel")

                try:
                    choice = int(input("\033[1;93mChoose :\033[0m\n"))
                except ValueError:
                    print("\033[1;91mENTER A VALID INPUT\033[0m\n")
                    utils.sleep(0.5)
                    continue

                if choice == 1:
                    file = utils.copy_file(file)
                    utils.sleep(0.5)
                    break # Leave the rename menu

                elif choice == 2:
                    file = utils.choose_file(files) # select another file

                elif choice == 3:
                   break

                else:
                    print("\033[1;91mENTER A VALID OPTION\033[0m\n")
                    utils.sleep(0.5)
                    continue

        elif "Copy Folder" in str(selected):
            folder = utils.choose_folder(folders) # For user to choose a file
            if file is None:
                continue # redraws the directory menu 

            while True:
                utils.clear()
                print("\033[1;93mSelected File:\033[0m")
                print(f"\033[1;97m{folder}\033[0m\n")
                utils.sleep(0.5)
                print("1.✅  Copy this folder")
                print("2.⬅️   Choose another folder")
                print("3.❌ Cancel")

                try:
                    choice = int(input("\033[1;93mChoose :\033[0m\n"))
                except ValueError:
                    print("\033[1;91mENTER A VALID INPUT\033[0m\n")
                    utils.sleep(0.5)
                    continue

                if choice == 1:
                    file = utils.copy_folder(folders)
                    utils.sleep(0.5)
                    break # Leave the rename menu

                elif choice == 2:
                    file = utils.choose_folder(folders) # select another file

                elif choice == 3:
                   break

                else:
                    print("\033[1;91mENTER A VALID OPTION\033[0m\n")
                    utils.sleep(0.5)
                    continue

        elif "Move File" in str(selected):

            file = utils.choose_file(files) # For user to choose a file
            if file is None:
                continue # redraws the directory menu 

            while True:
                utils.clear()
                print("\033[1;93mSelected File:\033[0m")
                print(f"\033[1;97m{file}\033[0m\n")
                utils.sleep(0.5)
                print("1.✅  Move this file")
                print("2.⬅️   Choose another file")
                print("3.❌ Cancel")

                try:
                    choice = int(input("\033[1;93mChoose :\033[0m\n"))
                except ValueError:
                    print("\033[1;91mENTER A VALID INPUT\033[0m\n")
                    utils.sleep(0.5)
                    continue

                if choice == 1:
                    file = utils.move_file(file)
                    utils.sleep(0.5)
                    break # Leave the rename menu

                elif choice == 2:
                    file = utils.choose_file(files) # select another file

                elif choice == 3:
                   break

                else:
                    print("\033[1;91mENTER A VALID OPTION\033[0m\n")
                    utils.sleep(0.5)
                    continue
        
        elif "Move Folder" in str(selected):
            folder = utils.choose_folder(folders) # For user to choose a file
            if folder is None:
                continue # redraws the directory menu 

            while True:
                utils.clear()
                print("\033[1;93mSelected File:\033[0m")
                print(f"\033[1;97m{file}\033[0m\n")
                utils.sleep(0.5)
                print("1.✅  Move this folder")
                print("2.⬅️   Choose another another")
                print("3.❌ Cancel")

                try:
                    choice = int(input("\033[1;93mChoose :\033[0m\n"))
                except ValueError:
                    print("\033[1;91mENTER A VALID INPUT\033[0m\n")
                    utils.sleep(0.5)
                    continue

                if choice == 1:
                    file = utils.move_folder(file)
                    utils.sleep(0.5)
                    break # Leave the rename menu

                elif choice == 2:
                    file = utils.choose_folder(folders) # select another file

                elif choice == 3:
                   break

                else:
                    print("\033[1;91mENTER A VALID OPTION\033[0m\n")
                    utils.sleep(0.5)
                    continue

        elif "Create Folder" in str(selected):
            utils.create_folder(current)
            continue

        elif "Create File" in str(selected):
            created = utils.create_file(current)
            if created is None:
                continue # return to the directory menu
        
        elif "Organize Files" in str(selected):
            organize(current)
