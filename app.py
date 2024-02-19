from flask import Flask, jsonify, request, render_template, flash, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename
import tensorflow as tf
from prediction import modele
from upload_BDD import upload_on_bdd
from descriptif import descriptif_table
from firebase_admin import credentials, storage, firestore
from table_user import table_user_id
import firebase_admin
from upload_nico import uploadImagesToFirebaseStorage
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
    global UID_user

    #Vérifier que la requête contient un JSON
    if request.is_json:

        #Obtenir les données JSON envoyées avec la requête
        data = request.get_json()

        #Extraire l'UID utilisateur du json reçu
        UID_user = data.get('uid', '')

        #Afficher l'UID utilisateur
        print(f"UID utilisateur reçu : {UID_user}")

        return jsonify({"message ": "UID reçu avec succès", "uid ": UID_user}), 200
    else :
        return jsonify({"error ": "Requête non JSON ou vide"}), 400
    
@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'Aucun fichier trouvé'}), 400
    photo = request.files['photo']
    if photo.filename == '':
        return jsonify({'error': 'Nom de fichier vide'}), 400

    if photo:
        filename = secure_filename(photo.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
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

@app.route('/bddnico')
def index():
    return render_template('/index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'photos' not in request.files:
        flash('Aucun fichier sélectionné')
        return redirect(request.url)
    
    photos = request.files.getlist('photos')
    animal = request.form['animal']  # Récupère le nom de l'animal sélectionné
    save_folder = 'dossier_images_download'

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    for photo in photos:
        if photo.filename == '':
            flash('Aucun fichier sélectionné')
            return redirect(request.url)
        if photo:
            filename = photo.filename
            destination = os.path.join(save_folder, filename)
            photo.save(destination)
            uploadImagesToFirebaseStorage(destination, animal)  # Passez l'animal en paramètre ici
    shutil.rmtree(save_folder)
    flash('Photos téléchargées avec succès')
    return redirect(url_for('index'))

@app.route('/pysparkus')
def index_pyspark():
    return render_template('/index1.html')

@app.route('/pyspark', methods=['POST'])
def pyspark_orchestrateur():

    #Mettre les scritps et fonctions de Nico pour déclencher PySpark et déclencher l'entraînement de l'IA à partir des i
#mages du dossier "dossier_images_download", enregistrer l'IA dans le dossier "IA" Supprimer le dossier contenant toutes
#les images sur le conteneur
    return

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)