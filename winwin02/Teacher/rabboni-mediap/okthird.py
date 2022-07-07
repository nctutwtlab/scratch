import asyncio
from rabboni_multi_python_sdk import Rabboni
import pyautogui
import time
import random

num_seconds=1
lx=0
ly=0
drags=0
choice=0
send=0
stime=0
count=0
flag=0

# send 開始執行，避免重複執行
# choice 是簡報還是 畫圖
# drags 是否拖拉滑鼠

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
    global now,drags,choice,send,stime,lx,ly,count,flag
    xOffset,yOffset=0,0
    x,y=0,0
    
    value_data = bytes(data).hex()

    acc_list = [convert_acc(value_data[:4], 2),  convert_acc(value_data[4:8], 2), convert_acc(value_data[8:12], 2)]
    gyr_list = [convert_gyr(value_data[12:16], 2),  convert_gyr(value_data[16:20], 2),
                    convert_gyr(value_data[20:24], 2)]
    cur_count = int(value_data[24:28], 16)
    stored_count = int(value_data[28:], 16)
    trigger = cal_trigger(acc_list)

    if flag==0:
        flag=1
        count=cur_count
        
    #print(acc_list[0] ,acc_list[1],acc_list[2], gyr_list[0],gyr_list[1],gyr_list[2],choice,sep="\t")
    #stime=time.sleep(2)
  
    if (choice==1):
        if trigger:
            if send==0:
                send=1
                pyautogui.press('F5')
                stime=time.time()
        if (acc_list[0]<-0.7 and abs(acc_list[1])<0.3 and abs(acc_list[2])<0.3):
            if send==0:
                send=1
                pyautogui.keyDown('shift')
                pyautogui.press('n')
                pyautogui.keyUp('shift')
                stime=time.time()
        elif (acc_list[0]>0.7 and abs(acc_list[1])<0.3 and abs(acc_list[2])<0.3):
            if send==0:
                send=1
                pyautogui.keyDown('shift')
                pyautogui.press('p')
                pyautogui.keyUp('shift')
                stime=time.time()
        elif (abs(acc_list[0])<0.3 and abs(acc_list[1])<0.3 and acc_list[2]<-0.7):
             if send==0:
                send=1           
                pyautogui.keyDown('ctrl')
                pyautogui.press('p')
                pyautogui.keyUp('ctrl')
                stime=time.time()
        elif (abs(acc_list[0])<0.3 and acc_list[1]<-0.7 and abs(acc_list[2])<0.3):
            drags=1
        elif (abs(acc_list[0])<0.3 and acc_list[1]>0.7 and abs(acc_list[2])<0.3):   
            drags=0
        if send==1:
            if ((time.time()-stime)>1.5):
                send=0
        
        if ((time.time()-now)>0.1):
            if (abs(acc_list[0])>0.2):
                xOffset=(-1)*acc_list[0]*50
            else:       
                xOffset=0
         
            if (abs(acc_list[1])>0.2):
                yOffset=1*acc_list[1]*50
            else:
                yOffset=0
                
            if xOffset!=0 or yOffset!=0:
                x,y= pyautogui.position()
                if ( x+xOffset<lx and  x+xOffset>0 and  y+yOffset<ly and y+yOffset>0 ):
                    if (drags): 
                        pyautogui.dragRel(xOffset, yOffset , button='left')
                    else: 
                        pyautogui.moveRel(xOffset, yOffset)
                     
               
    
    elif (choice==2):
        
         if  (acc_list[0]>-0.35 and acc_list[0]<0 and acc_list[1]<-0.9  and acc_list[1]>-1 and acc_list[2]<0.3 and acc_list[2]>0 and abs(gyr_list[0])<=10 and abs(gyr_list[1])<=10 and abs(gyr_list[2])<=10):
              if send==0 :
               send=1   
               print("renew") 
               pyautogui.doubleClick()    #重來
               stime=time.time() 
         elif  (acc_list[0]>-0.3 and acc_list[0]<=0.5 and acc_list[1]>0.7  and acc_list[1]<1 and acc_list[2]<0.3 and acc_list[2]>-0.3 and abs(gyr_list[0])<=10 and abs(gyr_list[1])<=10 and abs(gyr_list[2])<=10):
              if send==0:
               send=1   
               pyautogui.click()
               print("change")          #換顏色
               stime=time.time()
         elif   (acc_list[0]>-0.7 and acc_list[0]<1.4 and acc_list[1]>=-2  and acc_list[1]<=-0.7 and acc_list[2]<1.3 and acc_list[2]>0.5 and gyr_list[2]<=1000 and gyr_list[2]>500 ):
              if send==0:
               send=1   
               xOffset=gyr_list[2]*(-1)
               print("q left",xOffset)
               pyautogui.moveTo(random.randint(700,1250),random.randint(100,700))
               pyautogui.moveRel(random.randint(1,4),random.randint(1,4),0.4)
               k=random.randint(1,3)
               for i in range(k):
                  rx=random.randint(-200,-1)
                  ry=random.randint(-50,50)
                  x,y= pyautogui.position()
                  if (x+rx<lx and x+rx>0 and y+ry<ly and y+ry>0):
                     pyautogui.moveRel(rx,ry,random.uniform(0.1,0.3) )       # 快速往左
               count=cur_count      
               stime=time.time()
         elif   (acc_list[0]>-1.3 and acc_list[0]<1.2 and acc_list[1]>=-2  and acc_list[1]<=-1.4 and acc_list[2]<1.4 and acc_list[2]>0.5 and gyr_list[2]<-500 and gyr_list[2]>=-1000 ):
              if send==0:
               send=1   
               xOffset=gyr_list[2]*(-1)
               print("q right",xOffset)
               pyautogui.moveTo(random.randint(100,600),random.randint(100,700))
               pyautogui.moveRel(random.randint(1,4),random.randint(1,4),0.4)
               k=random.randint(1,3)
               for i in range(k):
                  rx=random.randint(1,200)
                  ry=random.randint(-50,50)
                  x,y= pyautogui.position()
                  if (x+rx<lx and x+rx>0 and y+ry<ly and y+ry>0):
                     pyautogui.moveRel(rx,ry,random.uniform(0.1,0.3))       # 快速往右
               count=cur_count      
               stime=time.time()
         elif cur_count>count:
             if send==0:
               send=1
               count=cur_count
               print("trigger",xOffset)
               m=random.randint(1,3)
               if m==1:
                   pyautogui.moveTo(random.randint(100,1250),random.randint(100,200))
                   pyautogui.moveRel(random.randint(1,4),random.randint(1,4),0.4)
                   k=random.randint(1,3)
                   for i in range(k):
                      rx=random.randint(-50,50)
                      ry=random.randint(1,150)
                      x,y= pyautogui.position()
                      if (x+rx<lx and x+rx>0 and y+ry<ly and y+ry>0):
                        pyautogui.moveRel(rx,ry,random.uniform(0.1,0.3))       # 快速上下
               elif m==2:
                   pyautogui.moveTo(random.randint(700,1250),random.randint(100,700))
                   pyautogui.moveRel(random.randint(1,4),random.randint(1,4),0.4)
                   k=random.randint(1,3)
                   for i in range(k):
                      rx=random.randint(-200,-1)
                      ry=random.randint(-50,50)
                      x,y= pyautogui.position()
                      if (x+rx<lx and x+rx>0 and y+ry<ly and y+ry>0):
                        pyautogui.moveRel(rx,ry,random.uniform(0.1,0.3) )       # 快速往左
               elif m==3:
                    pyautogui.moveTo(random.randint(100,600),random.randint(100,700))
                    pyautogui.moveRel(random.randint(1,4),random.randint(1,4),0.4)
                    k=random.randint(1,3)
                    for i in range(k):
                      rx=random.randint(1,200)
                      ry=random.randint(-50,50)
                      x,y= pyautogui.position()
                      if (x+rx<lx and x+rx>0 and y+ry<ly and y+ry>0):
                        pyautogui.moveRel(rx,ry,random.uniform(0.1,0.3))       # 快速往右
               stime=time.time()
 
         if send==1:
            if ((time.time()-stime)>=0.8):
                send=0      
               
          
               
             
         
     


def run():

    #mac1='EB:D8:2A:4D:1C:0A'
    #mac1='ED:11:4E:6A:97:0A'
    #mac1='C8:8F:50:D3:A1:05'
    mac1='E0:83:D3:BE:6C:BE'
  
    
    rab = Rabboni()
    mac=input('請輸入rabboni的MAC')
    if mac!='':
        mac1=mac
    tasks = [
            asyncio.ensure_future(rab.connect(mac_address=mac1,callback=_notify_callbackx))
        
    ]    
   
            
    
       
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

if __name__ == "__main__":
    try:
        lx,ly= pyautogui.size()
        now=time.time()
        print("x=",lx,"y=",ly)
        choice=int(input('請問要使用哪一種功能\n 1.簡報 \n 2.畫圖\n'))
        run()
    except KeyboardInterrupt:
        print('Bye~~')
