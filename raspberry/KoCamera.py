#from keras.models import load_model
from tensorflow.keras.models import load_model

from tensorflow import keras
#import raspberry.servo as sr
import tensorflow as tf
import numpy as np
import picamera
import imutils
import time
import PIL
import cv2
import os
#model = load_model('model.h5', compile = False)
model = load_model('/home/pi/Desktop/RPB/raspberry/util/my_model2.h5')
class_names = ['biodegradable', 'none biodegradable', 'recyclable']

stop_run = False
sdThresh = 10
#font = cv2.FONT_HERSHEY_SIMPLEX

def distMap(frame1, frame2):
    """outputs pythagorean distance between two frames"""
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist


def predect(data_image):
        fr = keras.preprocessing.image.img_to_array(data_image)
        fr = tf.expand_dims(fr, 0) # Create a batch

        predictions = model.predict(fr)
        score = tf.nn.softmax(predictions[0])


        ##### motor condition here #####
        print("This image most likely belongs to {} with a {:.2f} percent confidence.".format(class_names[np.argmax(score)], 100 * np.max(score)))
        trash_type = class_names[np.argmax(score)]
        if trash_type == "none biodegradable":
            t = 3
        elif trash_type == "biodegradable":
            t = 2
        elif trash_type == "recyclable":
            t = 4
        return t

#capture video stream from camera source. 0 refers to first camera,
#1 referes to 2nd and so on.


def detectObject(bol):
    global stop_run
    stop_run = bol
    cap = cv2.VideoCapture(0)
    frame_rate = 10
    prev = 0
    _, frame1 = cap.read()
    _, frame2 = cap.read()

    while stop_run:
        cv2.imshow('Trash Detection', frame2)
        time_elapsed = time.time() - prev
        _, frame3 = cap.read()
        #rows, cols, _ = np.shape(frame3)
        dist = distMap(frame1, frame3)

        frame1 = frame2
        frame2 = frame3

        # apply Gaussian smoothing
        mod = cv2.GaussianBlur(dist, (9,9), 0)
        # apply thresholding
        _, thresh = cv2.threshold(mod, 100, 255, 0)
        # calculate st dev test
        _, stDev = cv2.meanStdDev(mod)
        #cv2.imshow('dist', mod)

        if stDev > sdThresh:
            data_image = cv2.resize(frame3,(180,180))
            #time.sleep(5)
            if time_elapsed > 1./frame_rate:
                prev = time.time()
                trash_ID = predect(data_image)
                #sr.trashDump(trash_ID)
                break
        else:
            print("No Trash...")

        #cv2.putText(frame2, "Standard Deviation - {}".format(round(stDev[0][0],0)), (70, 70), font, 1, (255, 0, 255), 1, cv2.LINE_AA)

        if cv2.waitKey(1) & 0xFF == 27: break

    cap.release()
    cv2.destroyAllWindows()

while True:
    detectObject(True)