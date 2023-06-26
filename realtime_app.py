# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 12:34:15 2023

@author: hp
"""

import os
from flask import Flask,request,render_template,send_file,session

from werkzeug.utils import secure_filename
import io
import base64
import cv2
import numpy as np
import json

app = Flask(__name__)
app.secret_key = 'abcd'

@app.route('/')
def index():
    return render_template('index_realtime.html')

@app.route('/Caliberate')
def Caliberate():
    session.clear()  # Clear the session data
    return render_template('Caliberate.html')

@app.route('/upload', methods=['POST'])
def upload():
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
        
        contours_list = [contour.tolist() for contour in contours]
        num_contours=len(contours_list)
        
        destination_dir = 'upload'
        os.makedirs(destination_dir, exist_ok=True)  # Create directory if it doesn't exist
        image_path = os.path.join(destination_dir, filename + '.png')
        cv2.imwrite(image_path, binary_mask) 
        
        destination_dir_org = 'static/org_image'
        os.makedirs(destination_dir_org, exist_ok=True)  # Create directory if it doesn't exist
        image_path_org = os.path.join(destination_dir_org, filename)
        cv2.imwrite(image_path_org, image1) 
        
        # Convert the contours to nested lists
     
        # Store the necessary data in the session
        
        image2 = cv2.imread(image_path)
        img = cv2.cvtColor(image2,cv2.COLOR_BGR2GRAY)
        contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        #Reverting the original image back to BGR so we can draw in colors
        img_c = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        img_c1=cv2.drawContours(img_c, contours, -1, (0, 255, 0), 3)
        if image2 is None or contours is None:
         
            return "Image or contours data not found in the session"
        
        # Perform the remaining operations
        # Iterate over each contour
        
        # Sort the contours by area in descending order
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        L=[]
        W=[]
        for i, contour in enumerate(contours):
            # Create a blank image for the contour
            contour_image = np.zeros_like(image2)
           
            cv2.drawContours(contour_image, [contour], -1, (0, 255, 0), 2)
            x, y, width, height = cv2.boundingRect(contour)
            #perimeter = cv2.arcLength(contour, True)

            # Display the measured dimensions



            L.append(height)
            W.append(width)
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
            
        return render_template('Caliberate.html', num_contours=num_contours,length=L,width=W,filename=filename)




@app.route('/ViewCaliberate')
def ViewCaliberate():
    return render_template('ViewCaliberate.html')
  
@app.route('/RealTime')
def RealTime():
    return render_template('RealTime.html')

@app.route('/Statistics')
def Statistics():
    return render_template('Statistics.html')

if __name__ == '__main__':
    app.run(debug=True)