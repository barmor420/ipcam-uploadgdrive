# IPCAM upload to Google Drive

## A propos
Cet outil upload les fichiers images JPG issues d'une structure de sauvegarde IPCAM (recu par FTP par exemple)
exemple structure de répertoire IPCAM:
```
<repertoireRacine>/
    |-/20230310/
        |-/images/*.jpg
        |-/record/*.264
    |-/20230311/
        |-/images/*.jpg
        |-/record/*.264
```

## Installation

## Prérequis
environnement supporté: linux uniquement

python 3.7 ou supérieur

## Création et Activation de l'environnement virtuel Python
```
python3 -m venv env
```
```
source env/bin/activate
```

## Installation des librairies nécessaires (dans environnement virtuel)
```
pip --requirement requirements.txt
```
## Lancement du module dans l'environnement virtuel
```
source env/bin/activate
python main.py
```
# Configuration
Fichier _config.json_ à la racine du projet

```json
{
  "gdrive": {
    "oauth_credentials_file": "/home/barmor420/gdrive_token/code_secret_client_163499800699-37tntlgj0r3191dpvuopi7oqcspg0fss.apps.googleusercontent.com.json",
    "oauth_token_file": "/home/barmor420/gdrive_token/running_token.json",
    "folder_destination_id": "2dc4fGt6s34nUjml8fs3dDEtrcR510nhY"
  },
  "folder": {
    "source": "/home/barmor420/tests/camera/"
  }
}
```

_gdrive.oauth_credentials_file_ -> le fichier crédentiels OAuth
_gdrive.oauth_token_file_ -> le fichier de token
_gdrive.folder_destination_id_ -> l'id google drive du répertoire de destination

_folder.source_ -> le répertoire local contenant la structure IPCAM

Authentification oauth: suivre la documentation fournie par Google pour la génération du token
https://developers.google.com/drive/api/quickstart/python?hl=fr

## Packaging
Créer une archive contenant les scripts python pour distribution de l'application
le résultat est stocké dans dist
```
python -m build
```

# Troubleshoot
## Fail to create "failed to create interpreter directory not found"

Use pip tool to install the virtual environment
```
sudo apt install python3-pip python3-venv
```
