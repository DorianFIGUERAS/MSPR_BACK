# MSPR_BACK
# Back-End de l'application Wildlens


## Overview
Cette documentation a pour but d'être simple et d'expliquer l'installation de la partie Back-End de l'application Wildlens sur sa machine. Elle comprend l'installation d'un conteneur Docker et différents scripts python. 

## Requirements
Le projet requière plusieurs packages python :
- Flask
- Werkzeug
- Numpy
- Pillow
- Tensorflow
- Firebase-admin

## File Structure
- `app.py`: Main Flask application file.
- `descriptif.py`: Describes the application's functionalities.
- `index.html`, `index1.html`: Front-end HTML files.
- `prediction.py`: Handles the prediction logic.
- `requirements.txt`: Lists all the dependencies.
- `table_user.py`: Defines the user table schema.
- `upload_BDD.py`: Contains the logic for uploading to the database.
- `upload_nico.py`: Alternative script for database uploading.

## Setup Instructions
1. Ensure Docker is installed and running on your system.
2. Build the Docker container using the Dockerfile provided.
3. Install the required packages using `requirements.txt`.
4. Run `app.py` to start the Flask server.

## Usage
The application can be accessed via the front-end HTML pages which interact with the Flask backend for processing and predictions.

