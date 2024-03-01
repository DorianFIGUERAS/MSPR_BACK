# MSPR_BACK
# Back-End de l'application Wildlens


## Overview
Cette documentation a pour but d'être simple et d'expliquer l'articulation de la partie Back-End de l'application Wildlens sur sa machine. Elle comprend l'installation d'un conteneur Docker et différents scripts python. 

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

## Instructions
1. S'assurer que Docker est bien installé sur votre ordinateur (*[installer docker](https://www.docker.com/products/docker-desktop/)).
2. Via un invité de commande ou l'IDE de votre choix, lancer la commande ```docker build -t <nom_de_l'image_souhaitée> .```
3. Toujours via votre invité de commade ou via l'IDE de votre choix, exécuter la commande ```docker run --restart always -d -p 5000:5000 <nom_de_l'image_souhaitée>```
4. Accéder à l'url suivant pour vérifier que tout s'est bien exécuté : *[http://localhost:5000/upload_photo](http://localhost:5000/bddnico). Si vous arrivez sur une feêtre comme ceci c'est que cela a bien fonctionné : <img width="936" alt="image" src="https://github.com/DorianFIGUERAS/MSPR_BACK/assets/127091847/f311f762-706d-4b2d-be95-5a9bef0e80a9">



## Description détaillée des scripts
- **app.py** : Ce code Python est une application Flask qui fournit plusieurs endpoints pour différentes fonctionnalités, utilisant des bibliothèques externes. Import des bibliothèques et initialisation des variables :

  Importation des bibliothèques et configuration du certificat Firebase pour initialiser la connexion à la base de données.
  Initialisation de Flask avec une clé secrète. Déclaration des variables qui serviront comme 'UID_user'.
  Un dossier local est créé pour stocker les images téléchargées à partir de l'application.

  `/userid` : Reçoit et traite l'UID utilisateur envoyé sous forme de JSON par l'application.

  `/upload_photo` : Endpoint pour télécharger une photo envoyée par l'utilisateur, effectuer une prédiction à l'aide de l'appel de la méthode
"modele" du script **prediction.py**. On vient ensuite sauvegarder localement l'image, uploader les informations dans la base de données et exécuter la fonction "descriptif_table" du script **table_user.py** afin de récupérer les informations relatives à l'animal. On supprimer ensuite l'image enregistrée localement afin d'optimiser l'espace de stockage du serveur. Toutes ces informations sont renvoyées à l'application au format JSON et donc à l'utilisateur :  prédiction, descriptif de l'animal ainsi que l'url de la photo associé à l'animal prédit.

  `/history` : Endpoint pour récupérer l'historique des images téléchargées par un utilisateur. Grâce à la route '/userid' nous avons déjà récupérer l'UID de l'utilisateur lorsque il a démarrer l'application. Nous venons donc ici requpeter la base de données afin de récupérer l'historique de l'utilisateur (prédiction + photo envoyée) grâce à une clause where. Les données sont envoyées à l'application sous format JSON et affichées à l'utilisateur.

- **descriptif.py** :

    Importation des bibliothèques et définition des champs de la table "descriptif" dans la fonction **format_descriptif_data**. 

    **descriptif_table** : On définit un dictionnaire afin de récupérer l'animal ID correspondant à la prédiction effectuée (et récupérée en paramètre). On
    initialise la base de données, puis on requête la base de données grâce à l'ID de l'animal récupéré et aux champs de la table "descriptif" définit plus tôt.
    Toutes les informations sont retournées dans une variable dans le script **app.py**.


- **prediction.py** :
 
    Importation des bibliothèques.

    On vient charger le modèle d'IA déjà enregistré dans le conteneur Docker. La fonction **modele** attend en paramètre le path de l'image à classer. Pour cela, le script charge un fichier **class_names.json** également contenu dans le conteneur Docker qui contient les réponses possibles de classification. Ainsi, après analyse de l'image l'IA va retourner une prédiction ainsi que le pourcentage de chance que cette prédiction soit juste.

- **table_user.py** :

    Importation des bibliothèques
    Initialisation de la BDD si ce n'est pas déjà fait.
    
    On vient ici requêter la base de données Firebase afin de récupérer l'url des images uploadées par l'utilisateur ainsi que les prédictions associées. Cela permettra d'envoyer toutes ces informations à l'application au format JSON afin de les afficher à l'utilisateur.

- **TU.py** :

    Importation des bibliothèques.

    Ces tests sont voués à vérifier que l'ensemble des fonctions qui composent les différents scripts python sont fonctionnels et retournent bel et bien les réponses attendues.

- **upload_BBD.py** :

    Importation des bibliothèques et initialisation de la BDD si ce n'est pas déjà fait.

    Pour uploader l'image de l'utilisateur, nous récupérons ici le path de l'image initialement stockée dans le conteneur docker ainsi que l'UID de l'utilisateur. Nous envoyons ensuite l'image dans la BDD en spécifant que l'on souhaite créer une url publique associée à cette image afin de pouvoir la réutiliser plus tard (pour l'historique utilisateur par exemple). Une fois l'image uploadée ainsi que les informations créées, nous venons insérer tout cela dans la database de Firebase en spécifiant les champs ainsi que leur contenu.

  
    
