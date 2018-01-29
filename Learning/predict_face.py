# coding: utf-8

from keras.models import model_from_json
import cv2
import numpy as np
import pandas as pd


def face_extract(img):
    pixel = 300

    img = cv2.resize(img, (pixel, pixel))
    image_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # initialize face detector
    cascade_path = '../API/haarcascades/haarcascade_frontalface_alt.xml'
    cascade = cv2.CascadeClassifier(cascade_path)

    # Extract face image
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=2, minSize=(10, 10))

    if len(facerect) == 1:
        rect = facerect[0]

        # Remove image without face
        face = img[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]

        face = cv2.resize(face, (pixel, pixel))

        cv2.imwrite("./face.jpg", face)


def face_predict(img):

    """
    画像からラベルを予測

    img: face image

    label: star's label (ndarray)
    proba: all star probability (ndarray)
    max_indexes: top3 indexes (list)
    max_proba: top3 probability (list)
    """

    # Resize image to size of input layer
    img = cv2.resize(img, (100, 100))
    target = np.reshape(img, (1, img.shape[0], img.shape[1], img.shape[2])).astype('float') / 255.0

    json_string = open('../Learning/cnn_model.json').read()
    model = model_from_json(json_string)

    model.load_weights('../Learning/cnn_model_weight.hdf5')

    label = model.predict_classes(target)
    proba = model.predict_proba(target)[0]

    # Pick the TOP3 similar class index (Not sorted)
    unsorted_max_indexes = np.argpartition(-proba, 3)[:3]
    # y is array only TOP3 value
    y = proba[unsorted_max_indexes]
    indices = np.argsort(-y)
    max_indexes = unsorted_max_indexes[indices]

    max_proba_num = pd.DataFrame([proba[x] for x in max_indexes]).round(4)
    unformed_max_proba = max_proba_num.values

    top_k_indexes = max_indexes.tolist()
    top_k_proba = unformed_max_proba.T[0].tolist()

    return label, proba, top_k_indexes, top_k_proba


def age_gender_predict(img):

    """

    Predict Age & Gender
    [Warning]:  This use model_json file and model_weights.hdf5 file in age-gender-estimation.
                This learning color image. So that this functions img does not normalization.

    :param img: subject face image
    :return:    predicted genders
                predicted age
    """

    img = cv2.resize(img, (64, 64))
    target = np.reshape(img, (1, img.shape[0], img.shape[1], img.shape[2])).astype('float')

    json_string = open('../Learning/age_gender/age_gender_model.json').read()
    model = model_from_json(json_string)

    model.load_weights('../Learning/age_gender/age_gender_model.hdf5')

    label = model.predict(target)
    predicted_genders = label[0]

    ages = np.arange(0, 101).reshape(101, 1)
    predicted_ages = label[1].dot(ages).flatten()

    return predicted_genders, predicted_ages


if __name__ == '__main__':
    print("Please Exec Test Code")

    img = cv2.imread('../Learning/facedata/31/3.jpg')
    gender, age = age_gender_predict(img)
    print(gender)
    print(age)