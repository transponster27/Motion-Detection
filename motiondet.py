import cv2  #computer vision
import imutils    #frame manipulation, resizing

import threading  #camera display changes alarm data
import winsound   #alarm sound(windows) email,sms,call etc

video= cv2.VideoCapture(0, cv2.CAP_DSHOW)    #0 for one camera

video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


#compare one frame with another to calculate the differences, if high enough, alarm detects motion

_, start_frame = video.read()
start_frame = imutils.resize(start_frame, width= 500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)   #convert color bgr to grayscale
start_frame = cv2.GaussianBlur(start_frame, (21,21), 0)       #smoothen the frame

alarm = False
alarm_mode = False
alarm_counter = 0  #duration of movement before an alarm

def beep_alarm():                  #how to alert you
    global alarm
    for _ in range(5):
        if not alarm_mode:         #terminate alarm once you're alert
            break
        print("ALARM")
        winsound.Beep(2500, 100)   #5 consec beeps
    alarm = False    


while True:

    _, frame = video.read()
    frame = imutils.resize(frame,width=500)

    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(frame_bw, start_frame)                          #diff bw start and b/w frame
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]     #above 25- 255, below 25- 0
        start_frame = frame_bw 

        if threshold.sum() > 10000:         #motion sensitivity
            print(threshold.sum())
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1               #alarm only when motion is constant otherwise decrease the counter to avoid instant alarms

        cv2.imshow("Cam", threshold)             #b/w image
    else:
        cv2.imshow("Cam", frame)                 #original img


    if alarm_counter > 20:                       #duration before alarm
        if not alarm:
            alarm = True
            threading.Thread(target=beep_alarm).start()     #long duration of motion with alarm alert
        
    key_pressed = cv2.waitKey(30)                    
    if key_pressed == ord("v"):
        alarm_mode = not alarm_mode                   #toggle alarm
        alarm_counter = 0                             #reset
    if key_pressed == ord("q"):
        alarm_mode = False
        break

video.release()
cv2.destroyAllWindows()


