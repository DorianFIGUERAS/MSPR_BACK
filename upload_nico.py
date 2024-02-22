import os
from firebase_admin import storage, firestore, credentials
import firebase_admin

def uploadImagesToFirebaseStorage(images_path, animal_name):
    # Configuration Firebase
    firebase_config = {
        "type": "service_account",
        "project_id": "footprints-8e343",
        "private_key_id": "your_private_key_id",
        "private_key": "your_private_key",
        "client_email": "firebase-adminsdk@footprints-8e343.iam.gserviceaccount.com",
        "client_id": "your_client_id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk%40footprints-8e343.iam.gserviceaccount.com"
    }

    # Les IDs des animaux
    animal_ids = {
        "Castor": 1,
        "Chat": 2,
        "Chien": 3,
        "Coyote": 4,
        "Ecureuil": 5,
        "Lapin": 6,
        "Loup": 7,
        "Lynx": 8,
        "Ours": 9,
        "Puma": 10,
        "Rat": 11,
        "Raton laveur": 12,
        "Renard": 13
    }

    # Initialisation de Firebase
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_config)
        app = firebase_admin.initialize_app(cred, {
            'storageBucket': 'footprints-8e343.appspot.com'
        })
    else:
        app = firebase_admin.get_app()
    bucket = storage.bucket(app=app)
    db = firestore.client(app=app)

    # Vérifier si le chemin est un répertoire ou un fichier
    if os.path.isdir(images_path):
        images_paths = [os.path.join(images_path, f) for f in os.listdir(images_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    elif os.path.isfile(images_path) and images_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        images_paths = [images_path]  # Traiter le fichier directement si c'est une image
    else:
        print(f"Le chemin fourni n'est pas valide : {images_path}")
        return

    for image_path in images_paths:
        image_name = os.path.basename(image_path)
        blob = bucket.blob(f"Images/{animal_name}/{image_name}")
        blob.upload_from_filename(image_path)

            # Récupération de l'URL de téléchargement de l'image
        blob.make_public() # Rendre l'image publiquement accessible
        download_url = blob.public_url

            # Création d'un document Firestore avec les informations de l'image
        doc_data = {
            "animal": animal_name,
            "animal_id": animal_ids.get(animal_name, 0),  # Utiliser 0 si l'animal n'est pas trouvé
            "nom": image_name.split('.')[0],  # Nom de l'image sans extension
            "url": download_url  # URL publique de l'image
        }
        db.collection('images').add(doc_data)  # Ajouter le document à Firestore

        print(f"Image {image_name} téléchargée et enregistrée dans Firestore sous {animal_name}.")

    print("Toutes les images ont été traitées.")