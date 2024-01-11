from pathlib import Path
import unittest
import sys

sys.path.append("../")

from desktop_organizer.EventHandler import EventHandler
from watchdog.events import DirModifiedEvent

class TestSuite(unittest.TestCase):

    def setUp(self):
        self.src_root = Path.home() / "OneDrive/Desktop"
        self.dest_root = self.src_root / "Cleanup"
        self.folders = ["Documents", "Image", "Video"]
        self.event_handler = EventHandler(self.src_root, self.dest_root)

    def tearDown(self):

        """
        
        Removes files added by the test case to the destination directory

        """

        for folder in ["Documents", "Image", "Video"]:
            filepath = self.dest_root / folder
            for file in filepath.iterdir():
                file.unlink()

    # Create Files
    def create_files(self, files: list[str]):

        """
        
        Helper function that adds a list of files to the root directory.

        @param `Path src_root`: The directory that we observe for changes.
        @param `list[str] file`: The files to be added to the src_root directory.
        
        """

        for file in files:
            filepath = self.src_root / file
            filepath.touch()

    # Assert Files
    def assert_files(self, files: list[str]):

        """

        Helper function that verifies that the files where added to the correct destination sub directory.

        @param `list[str] files`: expected filepaths of the files added to the destination directory.
        
        """

        for file in files:
            filepath = self.dest_root / file
            self.assertTrue(filepath.exists())

    # Assert File Count
    def assert_file_count(self, file_count: list[int]):
        for expected_count, folder in zip(file_count, self.folders):
            folder_path = self.dest_root / folder
            count = len([file for file in folder_path.iterdir() if file.is_file()])
            self.assertEqual(count, expected_count)

    # Test Cases
    def test_single_media_single(self):
        self.create_files(["text.txt"])
        self.event_handler.on_modified(DirModifiedEvent)
        self.assert_files(["Documents/text.txt"])
        self.assert_file_count([1, 0, 0])
    
    def test_multiple_media_single(self):
        self.create_files(["text.txt", "image.jpg", "video.mp4"])
        self.event_handler.on_modified(DirModifiedEvent)
        self.assert_files(["Documents/text.txt", "Image/image.jpg", "Video/video.mp4"])
        self.assert_file_count([1, 1, 1])
    
    def test_single_media_multiple(self):
        self.create_files(["video.mp4", "video.mov"])
        self.event_handler.on_modified(DirModifiedEvent)
        self.assert_files(["Video/video.mp4", "Video/video.mov"])
        self.assert_file_count([0, 0, 2])
    
    def test_multiple_media_multiple(self):
        self.create_files(["image.jpg", "image.png", "image.gif", "video.mp4", "video.mov"])
        self.event_handler.on_modified(DirModifiedEvent)
        self.assert_files(["Image/image.jpg", "Image/image.png", "Image/image.gif", "Video/video.mp4", "Video/video.mov"])
        self.assert_file_count([0, 3, 2])

    def test_invalid_media(self):
        self.create_files(["audio.mp3"])
        self.event_handler.on_modified(DirModifiedEvent)
        self.assert_file_count([0, 0, 0])
    
    def test_invalid_and_valid_media(self):
        self.create_files(["audio.mp3", "text.txt"])
        self.event_handler.on_modified(DirModifiedEvent)
        self.assert_files(["Documents/text.txt"])
        self.assert_file_count([1, 0, 0])

if __name__ == "__main__":
    unittest.main()