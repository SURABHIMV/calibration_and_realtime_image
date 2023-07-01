* realtime_app.py(contains preprocessess_image function where it extracts the image through a POST request and performs image processing and after processing it stores the data such as (image paths, contour, etc) in the session and returns the num_contours value. and in caliberate.html this num_contour value is used in for loop such that based on each value's actual length and width inputted. and these values are stored in lists(in realtime_app.py function mask_image) and done other processing and stored some more data in the session and returns some data so that such information is used in tabular form in caliberate.html and also at the end included a submit button which will revert back to first page(where it contain all the buttons (calibrate,viewcaliberate, realtime, statistics). If I click on the viewcaliberate button a new page is opened where I can view the required calibrated information at the end also has a submit button which will revert back to the first page. if I click on the realtime a new page is opened where we get the information about the real-time image.
* templates folder( contain HTML files such as Calibrate, ViewCaliberate, RealTime,Statistics).HTML file should be in the template folder then only the Flask app will run.
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
watchdog==3.0.0

