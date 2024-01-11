from pathlib import Path
from time import sleep

from watchdog.observers import Observer

from desktop_organizer.EventHandler import EventHandler

if __name__ == '__main__':
    
    src_root = Path.home() / "OneDrive/Desktop"
    dest_root = src_root / "Cleanup"
    event_handler = EventHandler(src_root, dest_root)

    observer = Observer()
    observer.schedule(event_handler, src_root, recursive=True)
    observer.start()

    try:
        while True:
            sleep(60)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
