from rabboni import *
import sys
import time
from easytello import tello

#Tello連線
myTello = tello.Tello() #物件宣告


#Rabboni連線設定
rabbo = Rabboni(mode = "USB") #先宣告一個物件
rabbo.connect("F3:E6:9F:84:07:FD")#連接Rabboni
print ("Status:",rabbo.Status)

#Rabboni資料讀取
rabbo.read_data()

#等待Tello起飛手勢
print('系統啟動完成，Tello執行中')
while True:
    print('請進行起飛動作')
    if rabbo.Accz > 2.5:
        print("起飛並開啟影像串流")
        myTello.streamon()
        myTello.takeoff()#起飛
        time.sleep(3)#確保起飛時間及恢復動作
        break

#操作模式
while True:
    time.sleep(0.15)#減緩取樣頻率，避免過度取樣造成的動作
    if rabbo.Accz > 1.8 :
        if rabbo.Gyry < -60:
            print("左轉")
            myTello.ccw(90)
            time.sleep(1)#將手勢復原的時間
        elif rabbo.Gyry > 60:
            print("右轉")
            myTello.cw(90)
            time.sleep(1)
        elif rabbo.Accx < -3 and rabbo.Gyry < -30:
            print("上移")
            myTello.up(abs(int(rabbo.Accz)*20))
            time.sleep(1)
        elif rabbo.Accx > 3 and rabbo.Gyry > 30:
            print("下移")
            myTello.down(abs(int(rabbo.Accz)*20))
            time.sleep(1)
    if rabbo.Accx < -1.6 :
        if rabbo.Accz < -2.5 and rabbo.Gyry < -70:
            print("左移")
            myTello.left(abs(int(rabbo.Accx)*15))
            time.sleep(1)
        elif rabbo.Accz > 2.5 and rabbo.Gyry > 70:
            print("右移")
            myTello.right(abs(int(rabbo.Accx)*15))
            time.sleep(1)
        elif rabbo.Accy > 2.5 and rabbo.Gyrz > 70:
            print("前進")
            myTello.forward(abs(int(rabbo.Accx)*15))
            time.sleep(1)
        elif rabbo.Accy < -2.5 and rabbo.Gyry < -70:
            print("後退")
            myTello.back(abs(int(rabbo.Accx)*15))
            time.sleep(1)
    if rabbo.Accz <= -4 :
        break

myTello.land()#降落
myTello.streamoff()#關閉影像串流
print("空拍機降落並關閉影像串流")

#Rabboni斷開連結
rabbo.disconnect()
