# coding: utf-8

from keras.models import Sequential, model_from_json
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPool2D
import cv2
import numpy as np

def face_predict(img):

    # Resize image to size of input layer
    img = cv2.resize(img, (100, 100))
    target = np.reshape(img, (1, img.shape[0], img.shape[1], img.shape[2])).astype('float') / 255.0

    json_string = open('./cnn_model.json').read()
    model = model_from_json(json_string)

    model.load_weights('cnn_model_weight.hdf5')

    label = model.predict_classes(target)
    proba = model.predict_proba(target)

    return label, proba


if __name__ == '__main__':

    img_file = './facedata/26/6.jpg'

    img = cv2.imread(img_file)

    label, proba = face_predict(img)

    print(proba)
    print(proba.shape)
    print(label)