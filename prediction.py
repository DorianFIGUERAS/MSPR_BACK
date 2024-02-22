import numpy as np
import tensorflow as tf
import json
from flask import Flask, jsonify, request
import os
from werkzeug.utils import secure_filename
import sys


def modele(image_path):

    MODEL_PATH = 'IA'
    loaded_model = tf.keras.models.load_model(MODEL_PATH)

    img_height = 200
    img_width = 200

    with open('class_names.json', 'r') as file:
        class_names = json.load(file)

    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(img_height, img_width))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    prediction = loaded_model.predict(img_array)
    predicted_class_index = np.argmax(prediction)
    predicted_probability = round(np.max(prediction)*100)

    predicted_class = class_names[np.argmax(prediction)]


    return predicted_class, predicted_probability

