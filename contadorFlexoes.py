from operator import truediv
from pickle import TRUE
import cv2
import mediapipe as mp
import datetime

video = cv2.VideoCapture('flexao3.mp4')
pose = mp.solutions.pose
Pose = pose.Pose(min_tracking_confidence=0.5,min_detection_confidence=0.5)
draw = mp.solutions.drawing_utils
check = True
contador = 0
toggle = True

frames = video.get(cv2.CAP_PROP_FRAME_COUNT) 
fps = int(video.get(cv2.CAP_PROP_FPS)) 
seconds = int(frames / fps) 

print("duration in seconds:", seconds) 
start = datetime.datetime.now()


while True:
    frameatual = video.get(cv2.CAP_PROP_POS_FRAMES)
    tempo = int(frameatual/fps)
    end = datetime.datetime.now()
    print (f'{int((end - start).total_seconds())}')
    flexoesporseg = 0
    if tempo == 0:
        flexoesporseg = 0
    else: 
        flexoesporseg = contador/tempo
    success,img = video.read()
    videoRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = Pose.process(videoRGB)
    points = results.pose_landmarks
    if toggle:
        draw.draw_landmarks(img,points,pose.POSE_CONNECTIONS)
    h,w,_ = img.shape
    if points:
        NoDY = int(points.landmark[pose.PoseLandmark.NOSE].y*h)
        NoDX = int(points.landmark[pose.PoseLandmark.NOSE].x*w)
        maoDY = int(points.landmark[pose.PoseLandmark.RIGHT_INDEX].y*h)
        maoDX = int(points.landmark[pose.PoseLandmark.RIGHT_INDEX].x*w)
        maoEY = int(points.landmark[pose.PoseLandmark.LEFT_INDEX].y*h)
        maoEX = int(points.landmark[pose.PoseLandmark.LEFT_INDEX].x*w)
        Medmaos = (maoDY + maoEY)/2
    if True:
        dif = Medmaos- NoDY
        if check == True and dif >=210:
            check = False
        if check == False and dif <=100:
            contador +=1
            check = True
            print(f' contador {contador}')
        print(f' contador {contador}')
        print(f'dif {dif}')
    if toggle:
        cv2.rectangle(img,(10,250),(260,30),(61, 64, 61),-1)
        texto = f'Flex/s {"{:.2f}".format(flexoesporseg)}'
        cv2.putText(img, texto, (30, 200), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3)
        texto = f'Flex {contador}'
        cv2.putText(img,texto,(30,100),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3)   
        texto = f'Seg {tempo}'
        cv2.putText(img,texto,(30,150),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),3)   

        # 70 e 270 
        # 60 e -60      

    
    

    cv2.imshow('Resultado',img)
    
    key = cv2.waitKey(40)
    if key%256 == 27:
        break
    if key%256 == 9:
        toggle = not toggle