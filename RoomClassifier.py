import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

import glob
import os, sys
import cv2
from matplotlib import image
from PIL import Image
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from sklearn.preprocessing import StandardScaler


class RoomClassifier():
    
    def __init__(self, *args, **kwargs):

        batch_size = 510
        train_dir = 'ROBIN/'
        IMG_HEIGHT = 64
        IMG_WIDTH = 64
        
        scaler = StandardScaler()
        train_image_generator = ImageDataGenerator(rescale=1./255)

        train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                                directory=train_dir,
                                                                color_mode="grayscale",
                                                                shuffle=True,
                                                                target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                                class_mode='binary')
        # Data preprocessing (define images, targets, test images, test targets)
        images, targets = next(train_data_gen)
        images = images[:2000]
        images = images.reshape(-1, 64*64)
        images = images.astype(float)

        targets = targets[:2000]
        targets = np.where(targets==1, 0, targets) 
        targets = np.where(targets==2, 1, targets) 
        
        self.targets = np.where(targets==3, 2, targets) 
        self.images = scaler.fit_transform(images)
        self.images_test = np.array_split(images, 10)[-1]
        self.targets_test = np.array_split(targets, 10)[-1]

        #Init layers
        self.init_layers()
        self.init_train_parameters()

    def rotate_images(self):
        index = 0
        rooms_type = ['living_room', 'room', 'bath_room', 'toilets', 'kitchen']
        rooms_color = [(0,0,255), (0,255,0), (255 ,0 ,0), (255, 192, 203), (255,165,0)]
        
        for x in range(5):0
            current_folder = "ROBIN/module_base/*"
            for img in glob.glob(current_folder):
                for y in range(10000):
                    index += 1
                    im = cv2.imread(img)
                    img_rotate_90_clockwise = cv2.rotate(im, cv2.ROTATE_90_CLOCKWISE)

                    hsv = cv2.cvtColor(img_rotate_90_clockwise, cv2.COLOR_BGR2HSV)

                    # Define lower and uppper limits of what we call "brown"
                    brown_lo=np.array([0,0,0])
                    brown_hi=np.array([50,50, 50])

                    # Mask image to only select browns
                    mask = cv2.inRange(hsv,brown_lo,brown_hi)

                    # Change image to red where we found brown
                    im[np.where((im==[255, 255, 255]).all(axis=2))] = rooms_color[x]
                    print('changed')
                    cv2.imwrite("ROBIN/module/" + str(rooms_type[x]) + "/" + str(rooms_type[x]) + str(y) +".jpg", im)

    def init_layers(self):
        model = tf.keras.models.Sequential()

        # Add the layers
        model.add(tf.keras.layers.Dense(256, activation="relu"))
        model.add(tf.keras.layers.Dense(128, activation="relu"))
        model.add(tf.keras.layers.Dense(3, activation="softmax"))
        model_output = model.predict(self.images[0:1])
        self.model = model
    
    def init_train_parameters(self):
        self.model.compile(
            loss="sparse_categorical_crossentropy",
            optimizer="sgd",
            metrics=["accuracy"]
        )
        
    
    def train(self):
        history =  self.model.fit(self.images, self.targets, epochs=40, validation_split=0.2)
        self.model.save('house_plan_classifier.h5')
    
    def get_model(self):
        model = tf.keras.models.load_model("house_plan_classifier.h5")
        return model
    
    def predict(self, train_dir, batch_size, IMG_HEIGHT, IMG_WIDTH):
        model = tf.keras.models.load_model("house_plan_classifier.h5")

        scaler = StandardScaler()
        train_image_generator = ImageDataGenerator(rescale=1./255)
        train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                                directory=train_dir,
                                                                color_mode="grayscale",
                                                                target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                                class_mode='binary')

        # Data preprocessing (define images, targets, test images, test targets)
        images, targets = next(train_data_gen)
        images = images.reshape(-1, 64*64)
        images = images.astype(float)
        images = scaler.fit_transform(images)

        predictions = model(images)

        print(np.round(predictions))

if __name__ == "__main__":
    room_classifier = RoomClassifier()
    pass