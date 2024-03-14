from flask import Flask, jsonify, request, session
from flask_cors import CORS
import os
import json
import uuid
from werkzeug.utils import secure_filename
from prediction import modele
from upload_BDD import upload_on_bdd
from descriptif import descriptif_table
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

# Initialisation de Firebase
cred = credentials.Certificate('footprints.json')
initialize_app(cred, {'storageBucket': 'footprints-8e343.appspot.com'})
db = firestore.client()

app = Flask(__name__)
CORS(app)

app.secret_key = "secret_key_here"

UPLOAD_FOLDER = 'images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def unique_file_name(filename):
    base, extension = os.path.splitext(filename)
    unique_name = f"{base}-{uuid.uuid4()}{extension}"
    return unique_name

@app.route('/upload', methods=['POST'])
def upload_photo():
    # Vérifier si l'UID et la photo sont présents dans la requête
    if 'photo' not in request.files or 'uid' not in request.form:
        return jsonify({'error': 'UID ou fichier photo manquant'}), 400

    uid = request.form['uid']
    photo = request.files['photo']

    if photo.filename == '':
        return jsonify({'error': 'Nom de fichier vide'}), 400

    filename = secure_filename(photo.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_file_name(filename))
    photo.save(file_path)

    # Traitement de la photo (exemple fictif)
    prediction, pourcentage = modele(file_path)
    upload_image = upload_on_bdd(file_path, uid, prediction)
    valeurs, image_url = descriptif_table(prediction)

    os.remove(file_path)

    return jsonify({"Informations": valeurs, "pourcentage": pourcentage, "url": image_url}), 200


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