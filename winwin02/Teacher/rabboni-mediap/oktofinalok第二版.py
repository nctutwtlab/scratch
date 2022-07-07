import asyncio
from rabboni_multi_python_sdk import Rabboni
import pyautogui
import time


num_seconds=1
lx=0
ly=0
drags=0
choice=0
send=0
stime=0

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
    return round(x*gyr_scale/32768, precision)


def cal_trigger(acc_list):
    trigger_val = pow(acc_list[0], 2) + pow(acc_list[1], 2) + pow(acc_list[2], 2)
    # print(f'cal_trigger: {trigger_val}')
    return trigger_val > 2.5


def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
        val = val- (1  << bits)        # compute negative value
    return float(val)


      


def _notify_callbackx( sender, data):
    global now,drags,choice,send,stime,lx,ly
    xOffset,yOffset=0,0
    x,y=0,0
    
    value_data = bytes(data).hex()

    acc_list = [convert_acc(value_data[:4], 2),  convert_acc(value_data[4:8], 2), convert_acc(value_data[8:12], 2)]
    gyr_list = [convert_gyr(value_data[12:16], 2),  convert_gyr(value_data[16:20], 2),
                    convert_gyr(value_data[20:24], 2)]
    cur_count = int(value_data[24:28], 16)
    stored_count = int(value_data[28:], 16)
    trigger = cal_trigger(acc_list)

    
        
    print(acc_list[0] ,acc_list[1],acc_list[2], gyr_list[0],gyr_list[1],gyr_list[2],sep="\t")
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
                     
            now=time.time()      
    
    elif (choice==2):
         x,y= pyautogui.position()
         if ((time.time()-now)>0.1):
            if  (acc_list[0]>-0.3 and acc_list[0]<0 and acc_list[1]<-0.9  and acc_list[1]>-1 and acc_list[2]<0.3 and acc_list[2]>0):
               pyautogui.doubleClick()         
            elif  (acc_list[0]>-0.3 and acc_list[0]<0 and acc_list[1]>0.9  and acc_list[1]<1 and acc_list[2]<0.3 and acc_list[2]>0):
               pyautogui.click()
               time.sleep(1)
            elif  (acc_list[0]>0 and acc_list[0]<0.2 and acc_list[1]>-0.38  and acc_list[1]<0.1 and acc_list[2]<1 and acc_list[2]>0.9):
               xOffset=gyr_list[2]*(-1)
               if ( x+xOffset<lx and  x+xOffset>0  ):
                  pyautogui.moveRel(xOffset,0)
               elif x+xOffset>lx:
                  pyautogui.moveTo(lx,y)
               else:   
                  pyautogui.moveTo(0,y)
            now=time.time()      
     


def run():

    #mac1='EB:D8:2A:4D:1C:0A'
    mac1='C4:CF:43:07:96:AC'

  
    
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
        choice=int(input('請問要使用哪一種功能\n 1.簡報 \n 2.畫圖\n'))
        run()
    except KeyboardInterrupt:
        print('Bye~~')
