# https://t.ly/kE-O
import cv2
import mediapipe as mp
import numpy as np
import math
import pyautogui


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

ExAngle=40
ExStatus=False
countEx=0
pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=2,
        enable_segmentation=True,
        min_detection_confidence=0.5)


# For webcam input:
cap = cv2.VideoCapture(0)

with mp_pose.Pose(
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
      success, image = cap.read()
      if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue
      imgH,imgW=image.shape[0],image.shape[1]
      
      results = pose.process(image) #偵測身體
      #左手軸3點->11,13,15
      if (not results.pose_landmarks==None): #至少有一個身體
                
        #畫出點位
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks, #點
            mp_pose.POSE_CONNECTIONS, #連線
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
          )        
        image=cv2.flip(image, 1)
        # right hand
        x12,y12=round((1-results.pose_landmarks.landmark[12].x)*imgW),int(results.pose_landmarks.landmark[12].y*imgH)
        x14,y14=round((1-results.pose_landmarks.landmark[14].x)*imgW),int(results.pose_landmarks.landmark[14].y*imgH)
        x16,y16=round((1-results.pose_landmarks.landmark[16].x)*imgW),int(results.pose_landmarks.landmark[16].y*imgH)
        x24,y24=round((1-results.pose_landmarks.landmark[24].x)*imgW),int(results.pose_landmarks.landmark[24].y*imgH)
        x0,y0=round((1-results.pose_landmarks.landmark[0].x)*imgW),int(results.pose_landmarks.landmark[0].y*imgH)
        # left hand
        x11,y11=round((1-results.pose_landmarks.landmark[11].x)*imgW),int(results.pose_landmarks.landmark[11].y*imgH)
        x13,y13=round((1-results.pose_landmarks.landmark[13].x)*imgW),int(results.pose_landmarks.landmark[13].y*imgH)
        x15,y15=round((1-results.pose_landmarks.landmark[15].x)*imgW),int(results.pose_landmarks.landmark[15].y*imgH)
        x23,y23=round((1-results.pose_landmarks.landmark[23].x)*imgW),int(results.pose_landmarks.landmark[23].y*imgH)
        
        topl=120
        rightl=440
        leftl=100
        
        cv2.line(image, (leftl,topl), (leftl,imgH),  (255, 0, 255), 3)
        cv2.line(image, (rightl,topl), (rightl,imgH),  (255, 0, 255), 3)
        cv2.line(image, (leftl,topl), (rightl,topl),  (255, 0, 255), 3)
        
        if (x12<imgW and x12>0) and (y12<imgH and y12>0) and (x14<imgW and x14>0) and (y14<imgH and y14>0) and (x16<imgW and x16>0) and (y16<imgH and y16>0) and (x11<imgW and x11>0) and (y11<imgH and y11>0) and (x13<imgW and x13>0) and (y13<imgH and y13>0):          
          if (y16<60 and  abs(x12-x16)<=30  ):  #right hand raised
            cv2.putText(image,  str('change') , (30,40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)          
          elif ( y16<topl and (x16-x12)>40 ):  # top right  
            cv2.putText(image,  str('top right ') , (30,40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)          
          elif ( abs(y16-topl)<50 and  abs(x16-x0)<=24 ):  # top center 
            cv2.putText(image,  str('top center') , (30,40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
          elif ( abs(y16-topl)<=60 and  abs(x16-x11)<=35 ):  # top left 
            cv2.putText(image,  str('top left') , (30,40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)  
          elif ( abs(y16-y11)<=55 and  abs(x16-x11)<=55 ):  # middle left 
            cv2.putText(image,  str('middle left') , (30,40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
          elif ( abs(y16-y12)<75  and  x16>rightl ):  # middle right 
            cv2.putText(image,  str('middle right') , (30,40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)  
          elif ( abs(y16-y23)<140 and  x16-x23<=70  and  x16-x23>=-20):  # buttom left 
            cv2.putText(image,  str('buttom left') , (30,40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
          elif ( abs(y16-y24)<110 and  y16-y14>3 and  x16>rightl ):  # buttom right 
            cv2.putText(image,  str('buttom right') , (30,40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)     
          elif ( y16-y11>30 and y16-y11<150 and  abs(x16-x0-40)<=20):  # button center
            cv2.putText(image,  str('button center') , (30,40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)  
          elif ( abs(y16-y24)<45 and  (x16-x12)>15  and  (x16-x12)<60):  # reset 
            cv2.putText(image,  str('reset') , (30,40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)       

          
        
      cv2.imshow('MediaPipe Pose',image)
      if cv2.waitKey(5) & 0xFF == 27:
        break
cap.release()
