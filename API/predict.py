# coding: utf-8

# Add PATH of Project Directory
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import flask
from Learning.predict_face import face_predict, face_extract

import cv2
import pandas as pd

app = flask.Flask(__name__)

stars = pd.read_csv("./list.csv", header=None)

@app.route("/predict")
def predict():

    """
    API that returns similarity from facial images
    :return: json (star's label, similarity)
    """
    img_file = "./subject.jpg"
    img = cv2.imread(img_file)
    face_extract(img)

    face_file = './face.jpg'
    face = cv2.imread(face_file)

    label, proba, top_3, top_3_proba = face_predict(face)

    name_list = []

    for i in top_3:
        name = stars.loc[i][1]
        name_list.append(name)

    return flask.jsonify({
        "label": top_3,
        "probability": top_3_proba,
        "name": name_list
    })


if __name__ == "__main__":
    app.run(host="172.21.39.128", port=5000 ,debug=True)
