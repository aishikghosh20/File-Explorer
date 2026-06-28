import os, sys
from pathlib import Path
from time import sleep

def organize():
    
    # To get the directory of exe file
    if getattr(sys, "frozen", False):
        BASE_DIR = Path(sys.executable).parent 
    else:
        BASE_DIR = Path(__file__).parent


    # To scan the files in the folder



    # Creating folders with catgories 



    # Moving files in their appropriate folder



    # Duplicate deletion


    # Skipping System Folders



    # Progress Messages


    # Undo Previous 



    # Organize by
