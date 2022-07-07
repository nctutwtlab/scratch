from rabboni_multi_python_sdk import Rabboni
import asyncio
import pyautogui
import time
import random
import cv2
import mediapipe as mp
import numpy as np
import math

acc_list=[]
gyr_list=[]
cur_count=0
stored_count=0
trigger=0
ok=False
stime=0

def convert_acc(acc, acc_scale, precision=3):
    x = int(acc, 16)
    x = twos_comp(x, 16)
    x = float(x)
    # print('convert_acc', acc, x, acc_scale, x*(acc_scale)/32768)
    return round(x*(acc_scale)/32768, precision)  # x*16/32768


def convert_gyr(gyr, gyr_scale, precision=3):
    x = int(gyr, 16)
    x = twos_comp(x, 16)
    x = float(x)
    #print('convert_gyr', x, gyr_scale)
    return round(x*gyr_scale/32768*500, precision)


def cal_trigger(acc_list):
    trigger_val = pow(acc_list[0], 2) + pow(acc_list[1], 2) + pow(acc_list[2], 2)
    # print(f'cal_trigger: {trigger_val}')
    return trigger_val > 2.5


def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
        val = val- (1  << bits)        # compute negative value
    return float(val)


      


def _notify_callbackx( sender, data):
    global stime,acc_list,gyr_list,cur_count,stored_count,trigger,ok
    value_data = bytes(data).hex()

    acc_list = [convert_acc(value_data[:4], 2),  convert_acc(value_data[4:8], 2), convert_acc(value_data[8:12], 2)]
    gyr_list = [convert_gyr(value_data[12:16], 2),  convert_gyr(value_data[16:20], 2),
                    convert_gyr(value_data[20:24], 2)]
    cur_count = int(value_data[24:28], 16)
    stored_count = int(value_data[28:], 16)
    trigger = cal_trigger(acc_list)
    if trigger:
        if time.time()-stime>1:
            stime=time.time()
            pyautogui.moveRel(random.randint(-2,2),random.randint(-2,2),random.uniform(0.1,0.3))

    #print(acc_list[0] ,acc_list[1],acc_list[2], gyr_list[0],gyr_list[1],gyr_list[2],cur_count,stored_count,trigger,sep="\t")
               
             
async def test(): 

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
    status=0
    first=0
    second=0
    send=0
    state=0
    lx,ly=pyautogui.size()
    print(lx,ly)
    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:

        while cap.isOpened():
            await asyncio.sleep(0.1) 
            #if ok:
                #print(acc_list[0] ,acc_list[1],acc_list[2], gyr_list[0],gyr_list[1],gyr_list[2],cur_count,stored_count,trigger,sep="\t") 
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
                
                x12,y12=round((1-results.pose_landmarks.landmark[12].x)*imgW),int(results.pose_landmarks.landmark[12].y*imgH)
                x14,y14=round((1-results.pose_landmarks.landmark[14].x)*imgW),int(results.pose_landmarks.landmark[14].y*imgH)
                x16,y16=round((1-results.pose_landmarks.landmark[16].x)*imgW),int(results.pose_landmarks.landmark[16].y*imgH)
                x24,y24=round((1-results.pose_landmarks.landmark[24].x)*imgW),int(results.pose_landmarks.landmark[24].y*imgH)
                
                if (x12<imgW and x12>0) and (y12<imgH and y12>0) and (x14<imgW and x14>0) and (y14<imgH and y14>0) and (x16<imgW and x16>0)  :          
                    pyautogui.moveTo(x16*3,y16*9/4,random.uniform(0.1,0.2))
                    pyautogui.moveRel(random.randint(-2,2),random.randint(-2,2),random.uniform(0.1,0.2))
                   
                    
                    if (y16<100 and  abs(x12-x16)<=40  ):  #right hand raised
                        cv2.putText(image,  str('change') , (30,40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                        if send==0:  #換顏色
                            send=1   
                            pyautogui.moveTo(960,540)
                            pyautogui.click()
                            await asyncio.sleep(0.1)
                            send=0
                    elif ( abs(y16-y24)<45 and  (x16-x12)>15  and  (x16-x12)<60):  # reset 
                        cv2.putText(image,  str('reset') , (30,40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)       
                        if send==0 :
                            send=1   
                            pyautogui.moveTo(960,540)
                            pyautogui.doubleClick()    #重來 
                            await asyncio.sleep(0.1)
                            send=0     
                
                cv2.imshow('MediaPipe Pose',image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
        cap.release()
      #
   
def run():

    #mac1='EB:D8:2A:4D:1C:0A'
    #mac1='ED:11:4E:6A:97:0A'
    #mac1='C8:8F:50:D3:A1:05'
    #mac1='E0:83:D3:BE:6C:BE'
    mac1='C4:CF:43:07:96:AC'
    
    rab = Rabboni()
    mac=input('請輸入rabboni的MAC')
    if mac!='':
        mac1=mac
    tasks = [
            asyncio.ensure_future(rab.connect(mac_address=mac1,callback=_notify_callbackx)),
            asyncio.ensure_future(test())
        
    ]    
   
            
    
       
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
   
if __name__ == "__main__":
    try:
        lx,ly= pyautogui.size()
        print("x=",lx,"y=",ly)
        choice=int(input('請問要使用哪一種功能\n 1.簡報 \n 2.畫圖\n'))
        run()
    except KeyboardInterrupt:
        print('Bye~~')
