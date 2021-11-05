#!/usr/bin/env python
# coding: utf-8

# In[1]:

#the code needs  opencv, pyrebase4, datetime, replace  and Crypto packages.
# The Crypto Package has some uppercase and lower case problem which can be solved by renaming the folder name from python app data. 
from apscheduler.schedulers.blocking import BlockingScheduler
import cv2
import datetime
import re
import pyrebase


# In[2]:
#firebase api password is given to store the images into server.

firebaseConfig = {
  'apiKey': "AIzaSyB2Zj0g6nRECxBeZh1C2kinYhwQtttJvFk",
  'authDomain': "electric-meter-ocr.firebaseapp.com",
  'databaseURL': "https://electric-meter-ocr-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "electric-meter-ocr",
  'storageBucket': "electric-meter-ocr.appspot.com",
  'messagingSenderId': "607341385391",
  'appId': "1:607341385391:web:a02be3d2e8581bbc3fe65a",
  'measurementId': "G-W54XK4G6S7"
}


# In[3]:

#main funtion where data and time is recorded and the system will capture images in regular interval
def some_job():
  #capture the image from webcam port 0
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
  # time and data data is recorded
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

  # file name is saved with data and time and special char is replaced with white space
    file_name_first = re.sub('[!@#$/:]', '', date_time)
    print("date and time:",file_name_first)

  #image file name is finalized
    file_name=file_name_first+".png"
    print(file_name)

  #save the image into local device
    cv2.imwrite(file_name, image)

  #transfer image into the firebase server 
    firebase = pyrebase.initialize_app(firebaseConfig)
    storage = firebase.storage()
  #here child used for the local drive image name and put is used for target file name 
    storage.child(file_name).put(file_name)
    del(camera)

  #scheduler is defined to specify the interval of capturing the   
scheduler = BlockingScheduler()
scheduler.add_job(some_job, 'interval', seconds=10) #hours=1
scheduler.start()
