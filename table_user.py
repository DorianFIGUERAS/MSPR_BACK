import firebase_admin
from firebase_admin import credentials, firestore
import json

def table_user_id(user_id):

    # Vérifier si Firebase a déjà été initialisée
    if not firebase_admin._apps:
        # Initialisation de Firebase
        cred = credentials.Certificate("footprints.json")
        firebase_admin.initialize_app(cred)


    db = firestore.client()

    donnees_filtrees = []

    query = db.collection('images_user').where('user_id', '==', user_id)
    docs = query.stream()

    for doc in docs:
        doc_dict = doc.to_dict()
        donnees_filtrees.append({
            'url_image': doc_dict.get('url_image', 'Non fournie'),
            'prediction': doc_dict.get('prediction', 'Non fournie')
            })

    json_resultat = json.dumps(donnees_filtrees)
    return json_resultat