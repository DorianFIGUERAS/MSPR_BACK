import firebase_admin
from firebase_admin import credentials, firestore
import json

# Fonction pour formatter les données du document pour un affichage convivial
def format_descriptif_data(data):
    return {"Famille": data.get("descriptif_famille", ""),
            "Description": data.get("descriptif_description", ""),
            "Taille": data.get("descriptif_taille", ""),
            "Habitat": data.get("descriptif_habitat", ""),
            "Espèce": data.get("descriptif_espece", ""),
            "Région": data.get("descriptif_region", "")}

def descriptif_table(prediction):
    dictionnaire = {"castor": 1, "chat": 2}

    prediction_lower = prediction.lower()
    animal_id = dictionnaire[prediction_lower]

    # Vérifier si Firebase a déjà été initialisée
    if not firebase_admin._apps:
        # Initialisation de Firebase
        cred = credentials.Certificate("footprints.json")
        firebase_admin.initialize_app(cred)

    # Initialisation du client Firestore
    db = firestore.client()
    # Convertir animal_id en string pour créer l'ID du document
    document_id = f'descriptif{animal_id}'
    image_id = f'animal{animal_id}'


    # Tenter de récupérer le document dans la collection 'descriptif'
    descriptif_ref = db.collection('descriptif').document(document_id)
    doc = descriptif_ref.get()

    # Tenter de récupérer un document dans la collection 'images' correspondant à l'animal
    image_ref = db.collection('animal').document(image_id)
    image_doc = image_ref.get()

    if doc.exists and image_doc.exists:
         # Formatter les données pour l'affichage
        formatted_data = format_descriptif_data(doc.to_dict())
        # Construire la chaîne de valeurs
        valeurs = "\n".join(f"{key}: {value}\n" for key, value in formatted_data.items())
        # Récupérer l'URL de l'image
        image_url = image_doc.to_dict().get("animal_imageurl")
        return valeurs,image_url
    else:
        return (f"Aucun document trouvé pour animal_id: {prediction}")