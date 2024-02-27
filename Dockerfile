FROM python:3.11.5

# Définit le répertoire de travail
WORKDIR /python-docker

# Copiez d'abord le fichier requirements.txt et installez les dépendances.
# Cette étape est mise en cache tant que le fichier requirements.txt ne change pas.
COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip && \
    pip install -r requirements.txt

COPY prediction.py prediction.py
COPY app.py app.py
COPY class_names.json class_names.json
COPY IA IA
COPY upload_BDD.py upload_BDD.py
COPY footprints.json footprints.json
COPY descriptif.py descriptif.py
COPY table_user.py table_user.py



# Définit la commande par défaut pour exécuter l'application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]