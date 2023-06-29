* realtime_app.py(where extraction of image all preprocessing is done and stored in a folder and at time of flask application runtime this preprocessed image is extracted) and 
* templates folder( contain HTML files such as Calibrate, ViewCaliberate, RealTime,Statistics).HTML file should be in the template folder then only Flask app will run.
* data.text contains the dictionary format of data in which the key1 is (len_image name), value1 (multiplication factors of all contour length) and key2 is (wid_image_name) ,value2(multiplication factors of all contour width)
* data.text contains information about the image (images_top12.jpg)

#libraries versions used
Flask==2.2.2
gunicorn==20.1.0
Jinja2==3.1.2
numpy==1.21.6
pandas==1.3.5
Werkzeug==2.2.3
opencv-python==4.7.0.72
python version==3.8.16
spyder==5.4.2

