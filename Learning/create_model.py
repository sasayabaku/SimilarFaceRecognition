# coding:utf-8

from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPool2D
from keras.optimizers import Adam

from keras.layers.core import Dense, Activation, Dropout, Flatten
from keras.utils import plot_model
from keras.callbacks import EarlyStopping
from keras.utils import np_utils

import keras.callbacks
import keras.backend.tensorflow_backend as KTF
import tensorflow as tf

import os

import cv2
import numpy as np
from sklearn.model_selection import train_test_split

"""
Setting Parameter
img_row, img_cols: Neural Networkに入れる際の画像サイズ
img_channels: RGB画像なのでチャネル数が3
nb_classes: 芸能人のクラスラベル
nb_epoch: エポック数
"""

img_row, img_cols = 100, 100
img_channels = 3
nb_classes = 56
nb_epoch = 100

batch_size = 128


def loading_image():

    data_array = np.empty((0, img_row, img_cols, img_channels))
    label_array = np.empty((0, nb_classes))

    dir_path = "./facedata/"

    for classnum in range(nb_classes):
        file_list = os.listdir(dir_path + str(classnum))
        print(str(classnum) + ":--------------------")

        for file in file_list:
            print(str(file) + ":*********************")
            if file.endswith(".jpg"):

                orig_img = cv2.imread(dir_path + str(classnum) + '/' + str(file))
                img = cv2.resize(orig_img, (img_row, img_cols))
                float_img = np.reshape(img, (1, img.shape[0], img.shape[1], img.shape[2])).astype('float')
                train_data = float_img / 255.0
                train_label = np_utils.to_categorical(classnum, nb_classes)

                data_array = np.append(data_array, train_data, axis=0)
                label_array = np.append(label_array, [train_label], axis=0)

    return data_array, label_array


def learning_star(data, label):

    X_train, X_test, y_train, y_test = train_test_split(data, label, test_size=0.2, random_state=29)

    """
    Add TensorBoard
    """
    old_session = tf.Session('')
    session = tf.Session('')
    KTF.set_session(session)
    KTF.set_learning_phase(1)

    """
    Define the model
    """
    model = Sequential()

    model.add(Conv2D(30, 3, input_shape=(data.shape[1], data.shape[2], data.shape[3])))
    model.add(Activation('relu'))
    model.add(Conv2D(30, 3))
    model.add(Activation('relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Conv2D(30, 3))
    model.add(Activation('relu'))
    model.add(MaxPool2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(1024))
    model.add(Activation('relu'))
    model.add(Dropout(1.0))

    model.add(Dense(nb_classes, activation='softmax'))

    adam = Adam(lr=1e-4)

    model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=["accuracy"])

    """
    Add callbacks (TensorBoard, EarlyStopping)
    """
    tb_cb = keras.callbacks.TensorBoard('./logs/', histogram_freq=1)
    early_stopping = EarlyStopping(monitor='val_loss', mode='min', patience=20)
    cbks = [tb_cb, early_stopping]

    """
    Display Model Summary
    """
    plot_model(model, to_file='./model.png')


    """
    Learning Flow
    """
    history = model.fit(X_train, y_train, batch_size=batch_size, epochs=nb_epoch, verbose=1, validation_split=0.1, callbacks=cbks)
    score = model.evaluate(X_test, y_test, verbose=0)
    print('Test Score:', score[0])
    print('Test accuracy:', score[1])

    """
    Save Model
    """
    print('save the architechture of the model')
    json_string = model.to_json()
    open(os.path.join('./', 'cnn_model.json'), 'w').write(json_string)
    yaml_string = model.to_yaml()
    open(os.path.join('./', 'cnn_model.yaml'), 'w').write(yaml_string)

    print('save the weights')
    model.save_weights(os.path.join('./', 'cnn_model_weight.hdf5'))

    """
    Plot Learning log
    """
    # TensorBoard(log_dir='./logs')

    # KTF.set_session(old_session)


if __name__ == '__main__':
    data, label = loading_image()
    learning_star(data, label)
