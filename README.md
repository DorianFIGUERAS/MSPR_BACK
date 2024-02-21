# MSPR_BACK
# Back-End de l'application Wildlens


## Overview
Cette documentation a pour but d'être simple et d'expliquer l'installation de la partie Back-End de l'application Wildlens sur sa machine. Elle comprend l'installation d'un conteneur Docker et différents scripts python. 

## Requirements
Le projet requière plusieurs packages python qui seront installés via **requirements.txt** dans le conteneur Docker :
- Flask
- Werkzeug
- Numpy
- Pillow
- Tensorflow
- Firebase-admin

## Composition du repository
- `app.py`: Serveur Flask permettant l'accès au serveur et la mise en concordance des différents scripts python.
- `descriptif.py`: Permet de requêter la base de données Firebase en fonction de la prédiction faite par le script **prediction.py**. Ce script renvoie les informations relative à un animal ainsi qu'une URL qui correspond à l'image de l'animal prédit. 
- `index.html`, `index1.html`: Ce sont les Front-end HTML. **index.html** Permet d'uploader les images et de les classer dans différents dossier sur la base de données Firebase en fonction de l'animal sélectionné. **index1.html** permet d'éxécuter le script **pysparknico.py** afin de lancer la phase ETL et de lancer l'entraînement de l'IA via le script **entrainement.py**
- `prediction.py`: Ce script permet de faire une prédiction via le modèle d'IA enregistré dans le conteneur Docker en fonction de la photo envoyée par l'utilisateur.
- `requirements.txt`: Ce fichier contient la liste de toutes les dépendances python à installer dans le conteneur pour le bon fonctionnement.
- `table_user.py`: Ce script permet de récupérer toutes les urls des photos que l'utilisateur a envoyé au serveur ainsi que les prédictions faites par l'IA afin d'afficher un historique de prédiction à l'utilisateur côté application (front-end).
- `upload_BDD.py`: Contains the logic for uploading to the database.
- `upload_nico.py`: Alternative script for database uploading.

## Setup Instructions
1. Ensure Docker is installed and running on your system.
2. Build the Docker container using the Dockerfile provided.
3. Install the required packages using `requirements.txt`.
4. Run `app.py` to start the Flask server.

## Usage
The application can be accessed via the front-end HTML pages which interact with the Flask backend for processing and predictions.

