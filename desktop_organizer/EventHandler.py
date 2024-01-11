from watchdog.events import FileSystemEventHandler
from pathlib import Path
import shutil
import sys

from desktop_organizer.extensions import extensions

def rename_dest(file: Path, dest_root: Path) -> Path:

    """

    Helper function that renames file to new path. 
    
    If file of the same name already exists in the destination directory, 
    the file name is numbered and incremented until it's unique 
    (prevents overwriting files).

    @param `Path file`: path of file to move.
    @param `Path dest_root`: root path of destination directory.

    """
    
    dest = dest_root / file.name

    copies = 0

    while dest.exists():

        copies += 1

        dest = dest_root / f"{file.stem} ({copies}){file.suffix}"
    
    return dest

class EventHandler(FileSystemEventHandler):

    def __init__(self, src_root: Path, dest_root: Path):
        self.src_root = src_root.resolve()
        self.dest_root = dest_root.resolve()
    
    def on_modified(self, event):

        """

        Function that moves files from the source directory to the correct 
        destination sub directory whenever there is an on_modified event 
        triggered in the source directory.

        @param `DirModifiedEvent` or `FileModifiedEvent event`: event representing 
        file/directory modification.

        """

        for file in self.src_root.iterdir():
            if file.is_file() and file.suffix in extensions:
                src = file
                dest = self.dest_root / extensions[file.suffix]
                dest = rename_dest(file, dest)
                shutil.move(src, dest)