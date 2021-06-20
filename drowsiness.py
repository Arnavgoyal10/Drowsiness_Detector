import cv2
import numpy as np
import dlib
from imutils import face_utils
import datetime

cap = cv2.VideoCapture(0)

#Initializing the face detector and landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#status marking for current state
flag= 0
color=(0,0,0)
#how many times did a person blink
blink_count=0
#for how many frames were the eyes closed
blink1=0


normal = False
normal_count = 0.0
normal_eye_ratio = 0

_, frame = cap.read()
img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
font = cv2.FONT_HERSHEY_SIMPLEX


now = datetime.datetime.now()
CurrentTime= now.strftime("%Y-%m-%d %H:%M:%d")
cv2.putText(frame, "Sleep Detector: " + str(CurrentTime), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0xFF, 0xFF, 0xFF0), 2)
#function for distance 
def compute(ptA,ptB):
	dist = np.linalg.norm(ptA - ptB)
	return dist
#function for horizontal and vertical length ratio
def blinked(a,b,c,d,e,f):
	up = compute(b,d) + compute(c,e)
	down = compute(a,f)
	ratio = up/(2.0*down)
	return ratio
	

while True:
    _, frame = cap.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(img)
 
    #detected face in faces array
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        landmarks = face_utils.shape_to_np(predictor(img, face))

        # landmarks for the eyes
        left_blink = blinked(landmarks[36],landmarks[37], 
        	landmarks[38], landmarks[41], landmarks[40], landmarks[39])
        right_blink = blinked(landmarks[42],landmarks[43], 
        	landmarks[44], landmarks[47], landmarks[46], landmarks[45])
        # how much are the left and right eyes open on average
        eye_avg_ratio = (left_blink+right_blink) / 2.0


        if(not(normal)):
            if(normal_count<50):
                #find out the normal ratios of the eye when not blinking 
               normal_eye_ratio = normal_eye_ratio+eye_avg_ratio
            else:
                normal_eye_ratio = normal_eye_ratio/normal_count
                normal = True
                cv2.putText(frame, "Sleep Detector: " + str(CurrentTime), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0xFF, 0xFF, 0xFF0), 2)
 			    #repeat for 50 frames
            normal_count=normal_count+1        
        
        #Now judge what to do for the eye blinks
        if left_blink<0.2 and right_blink<0.2:
            blink1+=1
            if flag ==0:
                    blink_count+=1
                    flag=1
        else: 
            #flag to compare between the number of frames when the eye is closed and the number of times the eye is actually closed
            flag=0
               
                
        cv2.putText(frame,"The number of frames with closed eyes is " +str(blink1), (70,150), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
        cv2.putText(frame,"The number of times blinked is " +str(blink_count), (70,400), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
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