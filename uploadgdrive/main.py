# This is a sample Python script.
# Google drive
## https://developers.google.com/drive/api/quickstart/python
# Python project structure
## https://docs.python-guide.org/writing/structure/
## https://github.com/navdeep-G/samplemod
## Unit tests: https://realpython.com/python-testing/
##Dependency injections: https://python-dependency-injector.ets-labs.org/introduction/di_in_python.html

##Sample: https://github.com/dtsvetkov1/Google-Drive-sync

## https://linogaliana-teaching.netlify.app/bonnespratiques/

## https://packaging.python.org/en/latest/tutorials/packaging-projects/

# Python 3.7 compatibility (can be removed from Python 3.9)
from __future__ import annotations

import config
import googledrive
import miscellaneous
import pidfile
import os
import sys

from item import Item
from googleapiclient.discovery import Resource
from os import DirEntry
from pathlib import Path


def prevent_two_script_running():
    try:
        with pidfile.PidFile('/tmp/upload_gdrive.pid'): ## fixme: configure the pid file or put in a tmp location
            print('Process started')
    except SystemExit:
        sys.exit('script already running')


def list_files_to_upload(path: Path) -> list[DirEntry]:
    return miscellaneous.list_files_recursively_with_ext(path, 'jpg')


def list_upload_items(files: list[DirEntry]) -> list[Item]:
    items = list()
    for f in files:
        items.append(Item(f))
    return items


def initialise_google_drive() -> Resource:
    credentials_filename = config.get_gdrive_credentials_filename()
    token_file = config.get_gdrive_token_filename()
    gd_creds = googledrive.load_google_api_creds(credentials_filename, token_file)
    gd_service = googledrive.get_google_drive_service(gd_creds)
    return gd_service


def delete_file(item: Item):
    os.remove(item.get_file_path())


def upload_file(gd_service: Resource, item: Item):
    gd_folder_destination_id = config.get_gdrive_folder_destination_id()
    print(f"get/create: {item.get_parent_folder_name()}")
    parent_folder_id = googledrive.create_folder_if_not_exists(gd_service, item, gd_folder_destination_id)
    print(f"upload: {item.get_file_name()}")
    googledrive.upload_file(gd_service, item, parent_folder_id)


def upload_files(gd_service: Resource, items: list[Item]):
    for item in items:
        upload_file(gd_service, item)
        delete_file(item)


def main():
    prevent_two_script_running()
    folder_name = config.get_folder_source()
    folder_path: Path = miscellaneous.get_path(folder_name)
    files: list = list_files_to_upload(folder_path)
    if len(files) == 0:
        sys.exit("no file to upload")
    gd_service = initialise_google_drive()
    items = list_upload_items(files)
    upload_files(gd_service, items)


if __name__ == '__main__':
    main()
