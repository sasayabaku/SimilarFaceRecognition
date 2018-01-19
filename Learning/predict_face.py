# coding: utf-8

from keras.models import Sequential, model_from_json
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPool2D
import cv2
import numpy as np
import pandas as pd

def face_predict(img):

    """
    画像からラベルを予測

    img: face image

    label: star's label
    proba: all star probability
    max_indexes: top3 indexes
    max_proba: top3 probability
    """

    # Resize image to size of input layer
    img = cv2.resize(img, (100, 100))
    target = np.reshape(img, (1, img.shape[0], img.shape[1], img.shape[2])).astype('float') / 255.0

    json_string = open('./cnn_model.json').read()
    model = model_from_json(json_string)

    model.load_weights('cnn_model_weight.hdf5')

    label = model.predict_classes(target)
    proba = model.predict_proba(target)[0]

    # Pick the TOP3 similar class index
    max_indexes = np.argpartition(-proba, 3)[:3]

    max_proba_num = pd.DataFrame([proba[x] for x in max_indexes]).round(3)
    max_proba = max_proba_num.values

    return label, proba, max_indexes, max_proba


if __name__ == '__main__':

    img_file = './facedata/37/6.jpg'

    img = cv2.imread(img_file)

    label, proba, top_3, top_3_proba = face_predict(img)

    print(label)
    print(proba)
    print(top_3)
    print(top_3_proba)