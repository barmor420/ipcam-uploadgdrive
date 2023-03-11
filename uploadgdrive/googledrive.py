# Python 3.7 compatibility (can be removed from Python 3.9)
from __future__ import annotations

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.http import MediaFileUpload

from item import Item

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

# Globals
parent_folders_cache = {}


def load_google_api_creds(credentials_filename, token_filename) -> Credentials:
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_filename):
        creds = Credentials.from_authorized_user_file(token_filename, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_filename, SCOPES)  ## fixme file to locate properly
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_filename, 'w') as token:
            token.write(creds.to_json())
    return creds


def get_google_drive_service(creds: Credentials) -> Resource:
    service: Resource = build('drive', 'v3', credentials=creds)
    return service


def get_cache_id(folder_name: str, parent_folder_id: str) -> str:
    return folder_name + '__' + parent_folder_id


def get_folder_id_from_cache(folder_name: str, parent_folder_id: str) -> str:
    cache_id = get_cache_id(folder_name, parent_folder_id)
    folder_id = parent_folders_cache.get(cache_id)
    if not (folder_id is None):
        print(f"use cache for {folder_id} {folder_name}")
    return folder_id


def add_folder_id_to_cache(folder_name: str, parent_folder_id: str):
    cache_id = get_cache_id(folder_name, parent_folder_id)
    print(f"add to cache {parent_folder_id}")
    parent_folders_cache[cache_id] = parent_folder_id


def get_folder_id_from_drive(service: Resource, folder_name: str, parent_folder_id: str) -> str:
    response = service.files().list(
        q=f"name='{folder_name}' "
          f"and mimeType = 'application/vnd.google-apps.folder' "
          f"and '{parent_folder_id}' in parents",
        spaces='drive').execute()
    files = response.get('files', [])
    if len(files) > 0:
        return files[0].get('id')
    else:
        return ''


def get_folder_id(service: Resource, folder_name: str, parent_folder_id: str) -> str:
    folder_id = get_folder_id_from_cache(folder_name, parent_folder_id)
    if folder_id is None:
        folder_id = get_folder_id_from_drive(service, folder_name, parent_folder_id)
    return folder_id


def create_folder(service: Resource, folder_name: str, parent_folder_id: str) -> str:
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id]
    }
    file_drive = service.files().create(
        body=file_metadata,
        fields='id').execute()
    file_drive_id = file_drive.get('id')
    add_folder_id_to_cache(folder_name, file_drive_id)
    return file_drive_id


def create_folder_if_not_exists(service: Resource, item: Item, base_folder_id: str) -> str:
    parent_folder_name = item.get_parent_folder_name()
    parent_folder_id = get_folder_id(service, parent_folder_name, base_folder_id)
    if parent_folder_id == '':
        parent_folder_id = create_folder(service, parent_folder_name, base_folder_id)
    return parent_folder_id


def upload_file(service: Resource, item: Item, parent_folder_id: str) -> str:
    file_metadata = {
        'name': item.get_file_name(),
        'parents': [parent_folder_id]
    }
    media = MediaFileUpload(item.get_file_path(), mimetype='image/jpeg')
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id').execute()
    file_id = file.get('id')
    return file_id
