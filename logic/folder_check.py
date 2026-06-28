from time import sleep
from pathlib import Path
import stat
def should_skip(folder):
    attrs = folder.stat().st_file_attributes
    if not folder.is_dir():
        return False
    
    try :
        next(folder.iterdir(), None)
    except PermissionError:
        return True

    if attrs & stat.FILE_ATTRIBUTE_HIDDEN:
        return True

    if attrs & stat.FILE_ATTRIBUTE_SYSTEM:
        return True

    return False

