#!/usr/bin/env python
# coding: utf-8

# In[1]:


from apscheduler.schedulers.blocking import BlockingScheduler
import cv2
import datetime
import re
import pyrebase
import schedule
import time
import shutil
import os
import glob
import errno,stat


# In[2]:


#fire base API password
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


os.makedirs("Daily_img_data")
os.makedirs("Parant_img_data")


# In[ ]:


#function for capturing images 
def job_capture_img():
    
    #capture the image from webcam port 0
    
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    
    # time and data data is recorded
    
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    
    # file name is saved with data and time and special char is replaced with white space
    
    file_name_first = re.sub('[!@#$/: ]', '', date_time)
    print("date and time:",file_name_first)
    
    #image file name is finalized
    
    file_name=file_name_first+".png"
    print(file_name)
    
    #save the image into local device, one folder is for daily image another one is for 2/3 days old image
    cv2.imwrite("Parant_img_data/"+file_name, image)
    cv2.imwrite("Daily_img_data/"+file_name, image)
    del(camera)
    
def send_into_database():
    print("zip will be done and send the image into the database")
    
    #define the file name to upload into database as date_month_year
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y")
    file_name_to_upload = re.sub('[!@#$/: ]', '', date_time)
    #zip the daily image folder everyday one time
    shutil.make_archive("Daily_img_data", 'zip', "Daily_img_data/" )
    
    #initialize the firebase server
    firebase = pyrebase.initialize_app(firebaseConfig)
    storage = firebase.storage()
    
    #send into the database
    storage.child(file_name_to_upload+".zip").put("Daily_img_data"+".zip")
    print("upload_done")
    
    print("Delete daily file")
    os.remove("Daily_img_data.zip")
    shutil.rmtree("Daily_img_data/", ignore_errors=False, onerror=handleRemoveReadonly)
    os.makedirs("Daily_img_data")

def delete_old_folder():
    print("delete old folder")
    shutil.rmtree("Parant_img_data/", ignore_errors=False, onerror=handleRemoveReadonly)
    os.makedirs("Parant_img_data")
    print("deleted")
    
    
def handleRemoveReadonly(func, path, exc):
    
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
        func(path)
    else:
        raise

schedule.every(15).seconds.do(job_capture_img)
schedule.every().day.at("13:49").do(send_into_database)
schedule.every().day.at("13:52").do(delete_old_folder)


while True:
    schedule.run_pending()
    time.sleep(1) # wait one second


# import errno, os, stat, shutil
# 
# def handleRemoveReadonly(func, path, exc):
#     
#     excvalue = exc[1]
#     if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
#         os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
#         func(path)
#     else:
#         raise
# 
# shutil.rmtree("Daily_img_data/", ignore_errors=False, onerror=handleRemoveReadonly)

# %%
