# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 12:34:15 2023

@author: hp
"""

import os
from flask import Flask,request,render_template,send_file,session,redirect, url_for

from werkzeug.utils import secure_filename
from io import open
import io
import base64
import cv2
import numpy as np
import json
from PIL import Image


app = Flask(__name__)
app.secret_key = 'abcd' 

@app.route('/')
def index():
   
    return render_template('index_realtime.html')
    

@app.route('/Caliberate')
def Caliberate(): 
    return render_template('Caliberate.html')



@app.route('/preprocess_image', methods=['POST'])
def preprocess_image():
    if request.method == 'POST':
        # Retrieve the uploaded image file
        image_file = request.files['image']
        filename = secure_filename(image_file.filename)
        image1 = cv2.imread('images/' + filename)
        # Convert the image to grayscale
        gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        # Apply a threshold to create a binary image
        ret, binary_mask = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)

        # Find contours in the binary image
        contours, hierarchy = cv2.findContours(binary_mask,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
         
        
        destination_dir = 'upload'
        os.makedirs(destination_dir, exist_ok=True)  # Create directory if it doesn't exist
        image_path = os.path.join(destination_dir, filename + '.png')
        cv2.imwrite(image_path, binary_mask) 
        
        destination_dir_org = 'static/org_image'
        os.makedirs(destination_dir_org, exist_ok=True)  # Create directory if it doesn't exist
        image_path_org = os.path.join(destination_dir_org, filename)
        cv2.imwrite(image_path_org, image1) 
        
        # Convert the contours to nested lists
        contours_list = [contour.tolist() for contour in contours]
        # Store the necessary data in the session
        session['image1'] = image_path
        session['image_org']=image_path_org
        session['image_name']=filename
        session['num_contours'] = len(contours_list)

        #num_contours=len(contours_list)
        return render_template('Caliberate.html', num_contours=session['num_contours'])

    return render_template('Caliberate.html')


@app.route('/mask_image', methods=['POST'])
def mask_image():
    if request.method == 'POST':
        # Retrieve the user-submitted number of contours
        num_contours = session.get('num_contours')
        ln = []
        wd=[]
        for i in range(num_contours):
            length = request.form.get(f"length_{i}")
            width=request.form.get(f"width_{i}")
            
            if length is None:
                return f"length_{i} not provided"
            if width is None:
                return f"width_{i} not provided"
            ln.append(float(length))
            wd.append(float(width))
        if len(ln) != num_contours:
            return "Number of factors doesn't match the number of contours"

        ln = [float(l) for l in ln]
        wd = [float(w) for w in wd]

        # Retrieve the necessary data from the session
        image1 = session.get('image1')
        image2 = cv2.imread(image1)
        img = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        #Reverting the original image back to BGR so we can draw in colors
        img_c = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        img_c1=cv2.drawContours(img_c, contours, -1, (0, 255, 0), 3)
        if image2 is None or contours is None:
         
            return "Image or contours data not found in the session"
        
        filename = session.get('image_name')
        
        # Perform the remaining operations
        # Iterate over each contour
        
        # Sort the contours by area in descending order
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        L=[]
        W=[]
        MF_l=[]
        MF_w=[]
        d={}
    
        for i, contour in enumerate(contours):
    
            # Create a blank image for the contour
            contour_image = np.zeros_like(image2)
           
            cv2.drawContours(contour_image, [contour], -1, (0, 255, 0), 2)
            x, y, width, height = cv2.boundingRect(contour)
            #perimeter = cv2.arcLength(contour, True)

            # Display the measured dimensions
            w=width
            
            #print("Height: {} pixels".format(height))
            h=height
            m=ln[i]/h
            f=wd[i]/w
            MF_l.append(m)
            MF_w.append(f)

            L.append(h)
            W.append(w)
            
            
            key1='len'+'_'+str(filename)
            value1=MF_l
            key2='wid' +'_'+str(filename)
            value2=MF_w
            
            
            d[key1]=value1
            d[key2]=value2
            
            
            
            # Draw the contour and bounding box on the image (optional)
            #cv2.drawContours(contour_image, [contour], 0, (0, 255, 0), 2)
            cv2.rectangle(contour_image, (x, y), (x + width, y + height), (0, 0, 255), 2)

            # Draw the current contour on the image
            cv2.drawContours(contour_image, [contour], -1, (0, 255, 0), 2)
            # Create a text string with the dimensions
            
          
            # Save the modified contour image with a unique filename
            fname ='static/image'
            os.makedirs(fname, exist_ok=True)  # Create directory if it doesn't exist
            image_path = os.path.join(fname, f'contour_{i}' + '.png')
            cv2.imwrite(image_path, contour_image)
        
        with open('data.txt', 'a') as file:
        # Convert the dictionary to a JSON string
           json_data = json.dumps(d)

           # Write the JSON string to the file
           file.write(json_data + '\n')
        session['num_contours'] = num_contours
        session['length']=L
        session['width']=W
        session['actual_length']=ln
        session['actual_width']=wd
        session['MFL']=MF_l
        session['MFW']=MF_w
        
        return render_template('Caliberate.html', num_contours=num_contours,length=L,width=W,filename=filename,actual_length=ln,actual_width=wd,MFl=MF_l,MFw=MF_w)



@app.route('/ViewCaliberate')
def ViewCaliberate():
    num_contours=session.get('num_contours')
    filename = session.get('image_name')
    actual_length = session.get('actual_length')
    actual_width = session.get('actual_width')
    return render_template('ViewCaliberate.html',num_contours=num_contours, filename=filename, actual_length=actual_length, actual_width=actual_width)
  

@app.route('/RealTime')
def RealTime():
    return render_template('RealTime.html')

@app.route('/realtime_process', methods=['POST'])
def realtime_process():
    if request.method == 'POST':
        # Retrieve the uploaded image file
        image_file_real = request.files['image_p']
        filename_real = secure_filename(image_file_real.filename)
        image1 = cv2.imread('images/' + filename_real)
        # Convert the image to grayscale
        gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        # Apply a threshold to create a binary image
        ret, binary_mask = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)

        # Find contours in the binary image
        contours, hierarchy = cv2.findContours(binary_mask,cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
         
        
        destination_dir = 'upload/real_upload'
        os.makedirs(destination_dir, exist_ok=True)  # Create directory if it doesn't exist
        image_path = os.path.join(destination_dir, filename_real + '.png')
        cv2.imwrite(image_path, binary_mask) 
        
        
        image2 = cv2.imread(image_path)
        img = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        #Reverting the original image back to BGR so we can draw in colors
        img_c = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        img_c1=cv2.drawContours(img_c, contours, -1, (0, 255, 0), 3)
        if binary_mask is None or contours is None:
         
            return "Image or contours data not found in the session"
        
        
        # Perform the remaining operations
        # Iterate over each contour
        
        # Sort the contours by area in descending order
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        num_contours=len(contours)
        L=[]
        W=[]
        actualreal_l=[]
        actualreal_w=[]
        d={}
        key1='len'+'_'+str(filename_real)
        key2='wid' +'_'+str(filename_real)
        
        file_path = 'data.txt'  # Update with the correct file path

        with open(file_path, 'r') as file:
           data = file.read()
        dictionary = eval(data)   #if the dictionary data is stored in a string format in the text file, and you want to convert it back to a dictionary we use eval function
        v1=dictionary[key1]
        v2=dictionary[key2]
    
        for i, contour in enumerate(contours):
    
            # Create a blank image for the contour
            contour_image = np.zeros_like(image2)
           
            cv2.drawContours(contour_image, [contour], -1, (0, 255, 0), 2)
            x, y, width, height = cv2.boundingRect(contour)
            
            w=width
            
            #print("Height: {} pixels".format(height))
            h=height
            m=h*v1[i]
            f=w*v2[i]
            actualreal_l.append(m)
            actualreal_w.append(f)

            

            # Display the measured dimensions
            
            
            # Draw the contour and bounding box on the image (optional)
            #cv2.drawContours(contour_image, [contour], 0, (0, 255, 0), 2)
            cv2.rectangle(contour_image, (x, y), (x + width, y + height), (0, 0, 255), 2)

            # Draw the current contour on the image
            cv2.drawContours(contour_image, [contour], -1, (0, 255, 0), 2)
            # Create a text string with the dimensions
            
          
            # Save the modified contour image with a unique filename
            fname ='static/real_contour_image'
            os.makedirs(fname, exist_ok=True)  # Create directory if it doesn't exist
            image_path = os.path.join(fname, f'contour_{i}' + '.png')
            cv2.imwrite(image_path, contour_image)
        
        return render_template('RealTime.html', num_contours=num_contours,filename_real=filename_real,actualreal_l=actualreal_l,actualreal_w=actualreal_w)
         
        
       
        
        
       

@app.route('/Statistics')
def Statistics():
    return render_template('Statistics.html')

if __name__ == '__main__':
    app.run(debug=True)