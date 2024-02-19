import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import firestore

def upload_on_bdd(image_path, useruid, prediction):

    # Télécharger le fichier JSON de configuration Firebase depuis la console Firebase et le placer dans le répertoire d
#u script Python, on vérifie au préalable que Firebase admin n'est pas initiallisé:
    if not firebase_admin._apps:

        cred = credentials.Certificate("footprints.json")
        app = firebase_admin.initialize_app(cred, {
            'storageBucket': 'footprints-8e343.appspot.com'  # Remplacement avec le nom de notre bucket
            })
    else:
        app = firebase_admin.get_app()

    # Initialisation d'une référence au bucket Firebase Storage
    bucket = storage.bucket('footprints-8e343.appspot.com', app=app)

    # Chemin local vers l'image que l'on souhaite uploader
    chemin_image_locale = image_path

    # Nom que l'on souhaite donner à notre image dans Firebase Storage
    nom_image_storage = f"images_user/{image_path}"+f"USER{useruid}"

    # Upload de l'image vers Firebase Storage
    blob = bucket.blob(nom_image_storage)
    blob.upload_from_filename(chemin_image_locale)

    blob.make_public()

    # Obtention du lien de téléchargement de l'image uploadée
    lien_telechargement = blob.public_url

    db = firestore.client()

    #Création de la collection et du document
    doc_ref = db.collection('images_user').document()
    doc_ref.set({
        'url_image': lien_telechargement,
        'user_id': useruid,
        'prediction': prediction
        })


    return (f"Merci pour votre contribution à WildLens ! ")