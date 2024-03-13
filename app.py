from flask import Flask, jsonify, request, render_template, flash, redirect, url_for,session
import os
import json
import uuid
from werkzeug.utils import secure_filename
import tensorflow as tf
from prediction import modele
from upload_BDD import upload_on_bdd
from descriptif import descriptif_table
from firebase_admin import credentials, storage, firestore
from table_user import table_user_id
import firebase_admin
import shutil

cred = credentials.Certificate('footprints.json')
firebase_admin.initialize_app(cred,{
    'storageBucket': 'footprints-8e343.appspot.com',
    })

db = firestore.client()


app = Flask(__name__)

app.secret_key = "wildlens2024"
UID_user = ""
prediction = ""

UPLOAD_FOLDER = 'images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/userid', methods=['POST'])
def receive_uid():
    UID_user

    #Vérifier que la requête contient un JSON
    if request.is_json:

        #Obtenir les données JSON envoyées avec la requête
        data = request.get_json()

        #Extraire l'UID utilisateur du json reçu et le stocker dans la session
        session['UID_user'] = data.get('uid', '')

        #Afficher l'UID utilisateur
        print(f"UID utilisateur reçu : {session['UID_user']}")

        return jsonify({"message ": "UID reçu avec succès", "uid ": UID_user}), 200
    else :
        return jsonify({"error ": "Requête non JSON ou vide"}), 400

def unique_file_name(filename):
    base, extension = os.path.splitext(filename)
    unique_name = f"{base}-{uuid.uuid4()}{extension}"
    return unique_name
 
@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'Aucun fichier trouvé'}), 400
    photo = request.files['photo']
    if photo.filename == '':
        return jsonify({'error': 'Nom de fichier vide'}), 400

    if photo:
        filename = secure_filename(photo.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_file_name(filename)) #On s'assure ici que le nom de la photo est unique
        photo.save(file_path)
        prediction, pourcentage = modele(file_path)
        upload_image = upload_on_bdd(file_path, UID_user, prediction)
        valeurs, image_url = descriptif_table(prediction)
        os.remove(file_path)
        return jsonify({"Informations ": valeurs , "pourcentage ": pourcentage, "url ": image_url}), 200
    return jsonify({'error': 'Erreur lors du téléchargement'}), 500

@app.route('/history', methods=['POST'])
def get_table_user():

    data = request.get_json()

    user_id = data.get('uid', '')


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
            f"url_image": doc_dict.get('url_image', 'Non fournie'),
            f"prediction": doc_dict.get('prediction', 'Non fournie')
            })

    json_resultat = json.dumps(donnees_filtrees)
    return json_resultat


    return

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)