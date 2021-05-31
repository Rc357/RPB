# import the necessary packages
from keras.models import load_model 
from imutils.video import VideoStream
from tensorflow import keras
import tensorflow as tf
import numpy as np
import argparse
import datetime
import picamera
import imutils
import time
import PIL
import cv2
import os

### Load models and create classes ###
model = load_model('/home/pi/Desktop/RPB/raspberry/util/my_model2.h5')
#class_names = ['biodegradable', 'none biodegradable', 'recyclable']
class_names = ['biodegradable','recyclable']
#predection function
def predect(frame):
    fr = frame.copy()
    data_image = cv2.resize(fr,(180,180))

    fr = keras.preprocessing.image.img_to_array(data_image)
    fr = tf.expand_dims(fr, 0) # Create a batch

    predictions = model.predict(fr)
    score = tf.nn.softmax(predictions[0])

    ##### motor condition here #####
    print("This image most likely belongs to {} with a {:.2f} percent confidence.".format(class_names[np.argmax(score)], 100 * np.max(score)))


#def detect_Object():
vs = VideoStream(src=0).start()
#time.sleep(1.0)        
# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    frame = vs.read()
    text = "Unoccupied"
    print(text)
    
    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if frame is None:
        break
    
    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue
    
    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # loop over the contours
    for c in cnts:
        text = "Occupied"
        
    cv2.imshow("Trash Detection", frame)   
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)
    
    ### Predect the image in frame ###
    if text == "Occupied":
        #predect(frame)
        continue
        
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break

    
# cleanup the camera and close any open windows
vs.stop() if frame is None else vs.release()
cv2.destroyAllWindows()
