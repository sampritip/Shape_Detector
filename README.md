# Shape_Detector
Open a python IDE (Visual Studio Code preferably).\
Set up Anaconda in your system.\
Set up a python 3.9 virtual environment : conda create -n yourenvname python=3.9 anaconda\
Activate the virtual environment : conda activate yourenvname\
Clone this repository inside the virtual environment.\
The requirement.txt file contains the required dependencies and packages.\
"pip install -r requirements.txt" to get all the requirements.

If you have the hardware components available :\
Correctly specify the port number that the arduino is connected to.\
Connect then to your computer and run the arduino_test.py and servo_motor_test.py files to check if your arduino and servo motor are working.\
Set-up a camera. If you are using a built-in camera with your computer, change line number 12 \
'cap = cv2.VideoCapture(1)'\
to\
'cap = cv2.VideoCapture(0)'\
Finally run the 'contours_detection_servo_motor_control.py' script.

If you don't have the required hardware components, you can still run the script and check the output.\
Run the 'contours_detection_original.py' script.


