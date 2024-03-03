import os
from pathlib import Path


class Item:
    def __init__(self, file: os.DirEntry):
        self.file = file

    def get_file_path(self) -> str:
        return self.file.path

    def get_file_name(self) -> str:
        return self.file.name

    def get_parent_folder_name(self) -> str:
        return Path(self.file.path).parent.parent.name
