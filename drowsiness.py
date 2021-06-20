#Importing OpenCV Library for basic image processing functions
import cv2
# Numpy for array related functions
import numpy as np
# Dlib for deep learning based Modules and face landmark detection
import dlib
#face_utils for basic operations of conversion
from imutils import face_utils
import datetime
import time


#Initializing the camera and taking the instance
cap = cv2.VideoCapture(0)

#Initializing the face detector and landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#status marking for current state
flag= 0
color=(0,0,0)
blink_count=0
blink1=0
sleep_count = 0
max_sleep_count = 5

normal = False
normal_count = 0.0
normal_eye_ratio = 0

_, frame = cap.read()
img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
 # insert information text to video frame
font = cv2.FONT_HERSHEY_SIMPLEX


now = datetime.datetime.now()
CurrentTime= now.strftime("%Y-%m-%d %H:%M:%d")
cv2.putText(frame, "Sleep Detector: " + str(CurrentTime), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0xFF, 0xFF, 0xFF0), 2)
def compute(ptA,ptB):
	dist = np.linalg.norm(ptA - ptB)
	return dist

def blinked(a,b,c,d,e,f):
	up = compute(b,d) + compute(c,e)
	down = compute(a,f)
	ratio = up/(2.0*down)
	return ratio
	

while True:
    _, frame = cap.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(img)
    if(not(normal) and normal_count<47):

 # insert information text to video frame
    
        cv2.rectangle(img, (1, 50), (50, 80), (180, 132, 109), -1)
        cv2.putText(
            img,
            'ATTENTION PLEASE - Your activities are being logged',
            (60, 70),
            font,
            0.5,
            (0xFF, 0xFF, 0xFF),
            1,
            cv2.FONT_HERSHEY_SIMPLEX,
            )

    #detected face in faces array
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        landmarks = face_utils.shape_to_np(predictor(img, face))

        #The numbers are actually the landmarks which will show eye
        left_blink = blinked(landmarks[36],landmarks[37], 
        	landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42],landmarks[43], 
        	landmarks[44], landmarks[47], landmarks[46], landmarks[45])
        eye_avg_ratio = (left_blink+right_blink) / 2.0
        #print(eye_avg_ratio)
        if(not(normal)):
            if(normal_count<50):
               normal_eye_ratio = normal_eye_ratio+eye_avg_ratio
            else:
                normal_eye_ratio = normal_eye_ratio/normal_count
                normal = True
                cv2.putText(frame, "Sleep Detector: " + str(CurrentTime), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0xFF, 0xFF, 0xFF0), 2)
 			    #cv2.putText(frame, "LETS START!", (140, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (150, 0, 255), 3)
               # print(normal_eye_ratio)
            normal_count=normal_count+1        
        
   
        else:  
            if(normal_eye_ratio-eye_avg_ratio>0.5):
                sleep_count = sleep_count+1
                GPA=sleep_count/10
                
                
                if(sleep_count>max_sleep_count):
                     now = datetime.datetime.now()
                     CurrentTime= now.strftime("%Y-%m-%d %H:%M:%S")
                     cv2.putText(frame, "Sleep Detector: " + str(CurrentTime), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0xFF, 0xFF, 0xFF0), 2)
                     cv2.putText(frame, "Sleeping time (seconds):" + str("%6.0f " % GPA), (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0xFF, 0xFF, 0xFF0), 2)
                if ((GPA > 2) and (GPA < 5)):
                     cv2.putText(frame, "Alert! You should take a rest", (10, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                #print("Sleeping log - Time: " + str(CurrentTime) + " Duration: " + str("%6.0f" % GPA))
            else:
                sleep_count = 0

        
        #Now judge what to do for the eye blinks
        if left_blink<0.2 and right_blink<0.2:
            blink1+=1
            if flag ==0:
                    blink_count+=1
                    flag=1
        else: 
            flag=0
               
                
            

        cv2.putText(frame,"The number of frames with closed eyes is " +str(blink_count), (70,150), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
        cv2.putText(frame,"The number of times blinked is " +str(blink1), (70,400), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
        for n in range(0, 68):
            (x,y) = landmarks[n]
            cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)
			
		
     #show web cam frame 
    cv2.imshow("Frame", frame)
    if(normal_count==51):
        cv2.waitKey(1000)
        normal_count = 0
    else:
        wait = cv2.waitKey(1)
        if wait==ord("q"):
            cv2.destroyAllWindows()
            cap.stop()
            break