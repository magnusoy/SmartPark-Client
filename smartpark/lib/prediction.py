#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SmartPark - Client Application
Short description...

Code by: Magnus Øye, Dated: 14.12-2018
Contact: magnus.oye@gmail.com
Website: https://github.com/magnusoy/
"""

# Importing packages
from keras.preprocessing import image
from keras.models import model_from_json
import numpy as np
import glob


def loadModel():
    """Load trained model."""
    json_file = open('../model/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("../model/model.h5")
    print("Loaded model from disk")
    return loaded_model


def getParkingStatus(model):
    """Predict if the parkingslot is occupied or empty."""
    predictions = []
    path = '../instance/images/'
    for i, filename in enumerate(glob.glob(path + '*.png')):
        test_image = image.load_img(filename, target_size=(64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = model.predict(test_image)
        if result[0][0] == 1:
            prediction = True  # Occupied
        else:
            prediction = False  # Empty
        predictions.append(prediction)
    return predictions
