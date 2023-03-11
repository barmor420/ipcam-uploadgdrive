import json

# Global
config_json = None


def initialise_global() -> str:
    global config_json
    config_file = open('config.json', 'r')
    config_json = json.load(config_file)
    config_file.close()


def get_gdrive_credentials_filename() -> str:
    if config_json is None:
        initialise_global()
    return config_json['gdrive']['oauth_credentials_file']


def get_gdrive_token_filename() -> str:
    if config_json is None:
        initialise_global()
    return config_json['gdrive']['oauth_token_file']


def get_gdrive_folder_destination_id() -> str:
    if config_json is None:
        initialise_global()
    return config_json['gdrive']['folder_destination_id']


def get_folder_source() -> str:
    if config_json is None:
        initialise_global()
    return config_json['folder']['source']



