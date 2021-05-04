from rabboni import*
import turtle as tu
import time, sys
try:
    rabbo=Rabboni(mode="BLE")
except Exception as e:
    print(e)
    print("fail")
    sys.exit( )
    rabbo.scan() #掃描所有藍芽 Device
rabbo.print_device() # 列出所有藍芽 Device
rabbo.connect("E2:A4:E9:1D:38:D2")#依照 MAC 連接
rabbo.discover_characteristics()#掃描所有服務 可略過
rabbo.read_data()#讀取資料 必跑
x=-350
y=0
tu.pu()
tu.goto(x,y)
tu.pd()
tu.goto(350,0)
tu.pu()
tu.goto(x,y)
f=-320
tu.pd()
tu.hideturtle()
tu.speed(10)
a=rabbo.Accx
k=15 #可調整，警告數字
o=19 #可調整，計算數字
sea=0
tu.speed(5)
while True:
    for q in range(1,68): 
        a=rabbo.Accx
        tu.goto(f,10a)
        tu.forward(1)
        q+=1
        f+=10
        if a>o:
            print("Tsunami")
            sea+=1
        if a>k:
           print("wave")
        if sea>20:
            break
    if sea>20:
        break
    tu.clear()
    tu.pu()
    tu.goto(x,y)
    tu.pd()
    tu.goto(350,0)
    tu.pu()
    tu.goto(x,y)
    f=-290
    tu.pd()
#rabbo.stop()
print("run")
