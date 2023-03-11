# Python 3.7 compatibility (can be removed from Python 3.9)
from __future__ import annotations

import os
import pathlib


def get_current_path() -> pathlib.Path:
    """Get the current path of the executed py file"""
    return pathlib.Path(__file__).parent.resolve()


def get_path(path_string) -> pathlib.Path:
    """Get the current path of the executed py file"""
    return pathlib.Path(path_string).resolve()


def list_files_with_ext(path, ext) -> list[str]:
    """List the files of a path with a specific extension"""
    files = os.listdir(path)
    files_filtered = list(filter(lambda k: k.endswith(ext), files))
    return files_filtered


def list_files_recursively_with_ext(path, ext) -> list[os.DirEntry]:
    """List the files with a specific extension recursively from a defined path """
    files = list()
    with os.scandir(path) as it:
        ## TODO: manage this with lambda
        for entry in it:  # type: os.DirEntry
            if entry.is_dir() and not entry.name.startswith('.'):
                sub_folder_files = list_files_recursively_with_ext(entry, ext)
                files = files + sub_folder_files
            elif entry.is_file() and entry.name.lower().endswith(ext):
                files.append(entry)
    return files
