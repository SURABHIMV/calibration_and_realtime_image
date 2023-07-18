# Dimension measurement App 

This repository contains code for the calibration of images, viewing that processed image, and in real-time when an image is manually inputted how it gives the required result using the Flask application.


## Roadmap to reproduce the result
* In Anaconda create a new environment within this environment install all the required libraries as mentioned in (Libraries and Versions) and within this same environment open the IDE.

* In the local system create a new folder such that all the files which are to run in IDE are stored. Within this folder create a templates folder where all the required HTML files are stored. also, create folders for storing the original image, processed image, and real-time image separately. Create a text file(data.text) for storing the dictionary format of information where 'key' represents the image name, and 'value' contains the multiplication factors of all contours of that particular image.

* Using this 'key' value and the real-time image name is compared if there is any match then based on the 'value' which contains the multiplication factors of contours and the pixel value of contours obtained from the real-time image find the dimension of the real-time image object. if there is no match in the key and real-time image name then it will check with the next key value in the dictionary (data.txt) file. 

* Once the code and files are in the proper form we can run the realtime_app.py file and obtain a web link. When we run this web link 1st page is opened where we can see the Caliche logo, and client name at the top after that we can see the four buttons (Calibrate, View calibrate, Realtime, Statistics). When we click on Calibrate a new page is opened (where we can perform all the calibration operations and at the end, there is a button if we click on it can return to the first page).To view the calibration operation result click on the Viewcaliberate button, it opens a new page where we can see all the information in tabular format, and at the end, there is a button that will help to bring us back to the first page. To obtain real-time image dimension measurement click on the Realtime button which will open a new page (based on the real-time image in a particular folder, it will automatical access each image shows its dimension measurement details in tabular format).

## Files

* `realtime_app.py`: Contains the 'preprocess_image' function that extracts an image through a POST request, performs image processing, and stores relevant data (image paths, contours, etc.) in the session. It returns the num_contours value.
  
* `index_realtime.html`(1st page of the app): Contain code such that the first page of the app is visualized which contains 4 buttons(Caliberate, View calibrate, Realtime, Statistics).

* `Caliberate.html`(2nd page of app): The num_contour value (obtain from realtime_app.py function 'preprocess_image').This 'num_contour' value is used in a for loop such that based on each value actual length and actual width are manually inputted. These values are stored in lists in the mask_image function of realtime_app.py and then perform other preprocessing and store some useful data in the session and return some data so that such information is used in tabular form in caliberate.html and also at the end in caliberate.html file included a submit button which reverts back to the first page where it contains all the buttons(calibrate, view calibrate, realtime, statistics).
  
* `ViewCaliberate.html`(3rd page of the app): Contain code such that to visualize the preprocessed image and dimension information(obtain in the calibration stage) in tabular format.
  
* `RealTime.html`(4th page of the app): contain code to visualize the real-time image dimension information in tabular format.
  
* `templates` folder: Contains HTML files such as 'Calibrate.html', 'ViewCaliberate.html', 'RealTime.html', and 'Statistics.html'. These files should be placed in the 'templates' folder for the Flask app to run correctly.
  
* `data.txt`: Contains a dictionary format of data. 'key1' represents the image name with its length, and 'value1' contains the multiplication factors of all contour lengths. 'key2' represents the image name with its width, and 'value2' contains the multiplication factors of all contour widths.
  
* `images_top12.jpg`: Image used in the application.


## Libraries and Versions

The following libraries and versions were used in this project:

* `Flask==2.2.2`
* `gunicorn==20.1.0`
* `Jinja2==3.1.2`
* `numpy==1.21.6`
* `pandas==1.3.5`
* `Werkzeug==2.2.3`
* `opencv-python==4.7.0.72`
* `python==3.8.16`
* `spyder==5.4.2`
* `watchdog==3.0.0`








