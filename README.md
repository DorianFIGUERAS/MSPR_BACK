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

- `upload_BDD.py`: Ce script permet d'enregistrer les images envoyées par l'utilisateur ainsi que la prédiction qui a été faite et l'UID de l'utilisateur qui permettra par la suite de requpeter la base de données Firebase pour récupérer un historique utilisateur. 

- `upload_nico.py`: En lien direct avec **index.html**, ce script permet d'uploader les images sélectionnées, de les insérer et de générer des urls dans la base de données Firebase demanière quasi-automatisée.

## Instructions
1. S'assurer que Docker est bien installé sur votre ordinateur (*[installer docker](https://www.docker.com/products/docker-desktop/)).
2. Via un invité de commande ou l'IDE de votre choix, lancer la commande ```docker build -t <nom_de_l'image_souhaitée> .```
3. Toujours via votre invité de commade ou via l'IDE de votre choix, exécuter la commande ```docker run --restart always -d -p 5000:5000 <nom_de_l'image_souhaitée>```
4. Accéder à l'url suivant pour vérifier que tout s'est bien exécuté : *[http://localhost:5000/bddnico](http://localhost:5000/bddnico). Si vous arrivez sur une feêtre comme ceci c'est que cela a bien fonctionné : ![image](https://github.com/DorianFIGUERAS/MSPR_BACK/assets/127091847/ff00557a-6ab2-4883-85ef-49f2912c9fde)


## Description détaillée des scripts
- 'app.py' : Ce code Python est une application Flask qui fournit plusieurs endpoints pour différentes fonctionnalités, utilisant des bibliothèques externes. Import des bibliothèques et initialisation des variables :

  ## 1. Importation des bibliothèques et configuration du certificat Firebase pour initialiser la connexion à la base de données. Initialisation de Flask avec une clé secrète. Déclaration des variables qui serviront comme 'UID_user'. 
Un dossier local est créé pour stocker les images téléchargées à partir de l'application.

  ## 2. Définition des endpoints :

'/userid' : Reçoit et traite l'UID utilisateur envoyé sous forme de JSON par l'application.

'/upload_photo' : Endpoint pour télécharger une photo envoyée par l'utilisateur, effectuer une prédiction à l'aide de l'appel de la méthode "modele" du script **prediction.py**. On vient ensuite sauvegarder localement l'image, uploader les informations dans la base de données et exécuter la fonction "descriptif_table" du script **table_user.py** afin de récupérer les informations relatives à l'animal. On supprimer ensuite l'image enregistrée localement afin d'optimiser l'espace de stockage du serveur. Toutes ces informations sont renvoyées à l'application au format JSON et donc à l'utilisateur :  prédiction, descriptif de l'animal ainsi que l'url de la photo associé à l'animal prédit.

/history : Endpoint pour récupérer l'historique des images téléchargées par un utilisateur. Grâce à la route '/userid' nous avons déjà récupérer l'UID de l'utilisateur lorsque il a démarrer l'application. Nous venons donc ici requpeter la base de données afin de récupérer l'historique de l'utilisateur (prédiction + photo envoyée) grâce à une clause where. Les données sont envoyées à l'application sous format JSON et affichées à l'utilisateur.

/bddnico : Endpoint pour uploader les images sélectionnées dans la base de données afin d'alimenter plus tard pour l'ETL et l'entraînement de l'IA (page de téléversement d'images). Lors de l'envoie des images via le script **index.html**, cela va pointer vers l'endpoint '/upload' afin d'éxécuter l'insertion desimages dans la base de données. 

/upload : Endpoint pour uploader plusieurs photos dans la BDD. On les enregistre d'abord localement, puis on les uploade vers Firebase Storage avant de les supprimer du conteneur pour optimiser l'espace de stockage du serveur. 

/pysparkus : Endpoint pour rendre une autre page HTML (peut-être pour une interface utilisateur PySpark).

/pyspark : Endpoint pour déclencher un processus PySpark non défini dans ce code (probablement une tâche d'entraînement d'un modèle d'IA à partir des images téléchargées).

Fonctions associées à chaque endpoint :

Ces fonctions reçoivent généralement les données de requête, effectuent des opérations nécessaires, puis retournent une réponse appropriée (généralement au format JSON).
Des opérations telles que la manipulation de fichiers, les requêtes à une base de données Firestore, et les téléchargements vers Firebase Storage sont effectuées.
Exécution de l'application Flask :

L'application est exécutée sur 0.0.0.0 (pour écouter sur toutes les interfaces réseau) et le port 5000.
Le mode de débogage est activé pour faciliter le développement et le débogage.


