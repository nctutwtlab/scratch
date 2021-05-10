import tkinter as tk
from rabboni import *
global Keymax
global result
#---------------播放教學影片---------------------------------------------------------------
def video():
    import os, platform
    import vlc
    class Player:
    # args:設置 options
        def __init__(self, *args):
            if args:
                instance = vlc.Instance(*args)
                self.media = instance.media_player_new()
            else:
                self.media = vlc.MediaPlayer()

        def set_uri(self, uri):
            self.media.set_mrl(uri)

    # 播放 成功返回0，失敗返回-1
        def play(self, path=None):
            if path:
                self.set_uri(path)
                return self.media.play()
            else:
                return self.media.play()

    # 暂停
        def pause(self):
            self.media.pause()

    # 返回
        def resume(self):
            self.media.set_pause(0)

    # 停止
        def stop(self):
            self.media.stop()

    # 釋放資源
        def release(self):
            return self.media.release()

    # 是否正在播放
        def is_playing(self):
            return self.media.is_playing()

    # 已播放時間，返回毫秒值
        def get_time(self):
            return self.media.get_time()

    # 拖動指定的毫秒值處播放。成功返回0，失敗返回-1
        def set_time(self, ms):
            return self.media.get_time()

    # 聲音影片長度，返回毫秒值
        def get_length(self):
            return self.media.get_length()

    # 取得現在音量（0~100）
        def get_volume(self):
            return self.media.audio_get_volume()

    # 調整音量（0~100）
        def set_volume(self, volume):
            return self.media.audio_set_volume(volume)

    # 返回現在狀態：正在播放；暂停中；其他
        def get_state(self):
            state = self.media.get_state()
            if state == vlc.State.Playing:
                return 1
            elif state == vlc.State.Paused:
                return 0
            else:
                return -1

    # 現在播放進度。返回0.0~1.0浮點數
        def get_position(self):
            return self.media.get_position()

    # 移動當前進度，傳入0.0~1.0之間的浮點數
        def set_position(self, float_val):
            return self.media.set_position(float_val)

    # 取得當前播放速率
        def get_rate(self):
            return self.media.get_rate()

    # 設定播放速率（如：1.2，表示加速1.2倍播放）
        def set_rate(self, rate):
            return self.media.set_rate(rate)

    # 設置寬高比（如"16:9","4:3"）
        def set_ratio(self, ratio):
            self.media.video_set_scale(0)  # 必須設置為0，否則無法修改螢幕寬高
            self.media.video_set_aspect_ratio(ratio)

    # 設置窗口句柄
        def set_window(self, wm_id):
            if platform.system() == 'Windows':
                self.media.set_hwnd(wm_id)
            else:
                self.media.set_xwindow(wm_id)

    # 加入監聽器
        def add_callback(self, event_type, callback):
            self.media.event_manager().event_attach(event_type, callback)

    # 移除監聽器
        def remove_callback(self, event_type, callback):
            self.media.event_manager().event_detach(event_type, callback)

    import tkinter as tk
    global Keymax

    class App(tk.Tk):
        def __init__(self):
            super().__init__()
            self.player = Player()
            self.title("地震波介紹影片")
            self.create_video_view()
            self.create_control_view()

        def create_video_view(self):
            self._canvas = tk.Canvas(self, bg="#FFFF93")
            self._canvas.pack()
            self.player.set_window(self._canvas.winfo_id())

        def create_control_view(self):
            frame = tk.Frame(self)
            tk.Button(frame, text="播放", bg="#FFC9C9",command=lambda: self.click(0)).pack(side=tk.LEFT, padx=5)
            tk.Button(frame, text="暫停", bg="#FFC9C9",command=lambda: self.click(1)).pack(side=tk.LEFT)
            tk.Button(frame, text="停止", bg="#FFC9C9",command=lambda: self.click(2)).pack(side=tk.LEFT, padx=5)
            frame.pack()
       
        def click(self, action):
            global Keymax
            if action == 0:
                if self.player.get_state() == 0:
                    self.player.resume()
                elif self.player.get_state() == 1:
                    pass  # 播放新资源
                else:
#全域變數 Keymax  0: P wave , 1:S wave , 2:Love wave , 3:Rayleight wave
                    if Keymax == 0:
                        self.player.play("./pwave.mp4")
                    elif Keymax == 1:
                        self.player.play("./swave.mp4")
                    elif Keymax == 2:
                        self.player.play("./lovewave.mp4")
                    elif Keymax == 3:
                        self.player.play("./raywave.mp4")
#                    self.player.play("https://www.youtube.com/watch?v=VbfpW0pbvaU")
            elif action == 1:
                if self.player.get_state() == 1:
                    self.player.pause()
            else:
                self.player.stop()

    if "__main__" == __name__:
        app = App()
        app.mainloop()
        
#-----------機器學習-人工智慧分析-------------------------------------------------------------

def SVM():
    
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    import pandas as pd
    global Keymax

    df = pd.read_csv('./20210328train.csv')
    X = df.iloc[:, 1:7]
    Y = df.iloc[:, 7]
    print(X)
    print(Y)

#訓練資料與測試資料，訓練資料用在訓練模型的時候，測試則用來測試這個模型預測的準確度。
    from sklearn.model_selection import train_test_split
    x_train,x_test,y_train,y_test = train_test_split(X, Y, test_size=0.2)

    from sklearn import svm
    sv = svm.SVC()
    sv.fit(x_train, y_train)
    #print(sv)
#準確度分析   
    print(sv.score(X, Y))
    print(sv.score(x_train,y_train))
    print(sv.score(x_test, y_test))
#導入測試資料，進行預測
    dfa = pd.read_csv('./20210328test.csv')
    Xa = dfa.iloc[:, 1:7]
    #Ya = dfa.iloc[:, 7]
    x_traina,x_testa = train_test_split(Xa, test_size=0.9)
    preda = (sv.predict(x_testa))
    print(preda)
    print(type(preda))
    print(preda.dtype)
    #print(y_testa) 
#----------------------------------------------------------------   
    #NumPy Array to List   
    arr = np.array(preda)
    #原來Numpy陣列
    print(f'NumPy Array:\n{arr}')
    list1 = arr.tolist()
    #轉換為List
    print(f'List: {list1}')
    
#----------------------------------------------------------------    

    a = {}
    for i in list1:
        if list1.count(i)>0:
            a[i] = list1.count(i)
    print (a)
    
    c=dict(sorted(a.items(), key=lambda item: item[1]))
    print(c) 
    global Keymax
    Keymax = max(c, key=c.get) 
    print(Keymax)
    
#---------判斷地震波型--------------------------------------------------------------

    if(Keymax==0):
        print("P wave", end='')
        result.set("地震波 P 波")
        
    elif(Keymax==2):
        print("Love wave", end='')
        result.set("地震波 洛夫波")
       
    elif(Keymax==1):
        print("S wave", end='')
        result.set("地震波 S 波")
        
    elif(Keymax==3):
        print("Rayleight wave", end='')
        result.set("地震波 雷利波")
        
    else:
        print("無法判斷，請重新測試")

    
#-----------波形繪圖分析-------------------------------------------------------------

def analysis():
    import tkinter as tk
    import matplotlib.pyplot as plt   
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.backend_bases import key_press_handler
    from matplotlib.figure import Figure
    import pandas as pd
    import numpy as np
    from pandas import DataFrame
    
    frame1 = tk.Tk()
    frame1.title("地震波數據圖形分析")
    frame1.geometry("800x400")

    f = Figure(figsize=(5, 4), dpi=100)
    a = f.add_subplot(121)
    b = f.add_subplot(122)
    df=pd.read_csv('./20210328test.csv')
    
    df1=df.iloc[:,1:2]
    df2=df.iloc[:,2:3]
    df3=df.iloc[:,3:4]
    dfa=df.iloc[:,4:5]
    dfb=df.iloc[:,5:6]
    dfc=df.iloc[:,6:7]
    
    a.plot(df1,label="Ax")
    a.plot(df2,label="Ay")
    a.plot(df3,label="Az")
    b.plot(dfa,label="Gx")
    b.plot(dfb,label="Gy")
    b.plot(dfc,label="Gz")
    a.legend()
    b.legend()

    canvas = FigureCanvasTkAgg(f, master=frame1)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(canvas, frame1)
    toolbar.update()

    def on_key_event(event):
        print('you press %s' %event.key)
        key_press_handler(event, canvas, toolbar)

    canvas.mpl_connect('key_press_event', on_key_event)

    def _quit():
        frame1.quit()
        frame1.destroy()

    button = tk.Button(frame1, text='離開', command=_quit)
    button.pack(side=tk.BOTTOM)

    frame1.mainloop()
    
#----------------------測試資料擷取--------------------------------------------------------------------    
def start():
    import time, sys
    import pandas as pd
    import numpy as np
    import rabboni as rabbo
       
    try:
        result.set("資料擷取...!!")
        rabbo = Rabboni(mode = "BLE") #先宣告一個物件
        rabbo.scan() #掃描所有藍芽Device
#        rabbo.print_device() # 列出所有藍芽Device
        rabbo.connect("E0:34:CC:EF:22:F5")#依照MAC連接
#        rabbo.discover_characteristics()#掃描所有服務 可略過
#        rabbo.print_char()#列出所有服務 可略過
    
    except Exception as e:
        print(e)
        result.set("Rabboni藍芽連接失敗 !")
        print("可能你沒把 Rabboni 用藍芽連接好 !")
        sys.exit( )
        print ("Status:",rabbo.Status)
    
    i=1300
    df=pd.DataFrame(columns=('Ax','Ay','Az'))

    try:
        rabbo.read_data()   
        while True:#一直打印資料 直到結束程式
            result.set("資料傳輸中...!!")
            rabbo.print_data()#print 資料
#           print (rabbo.data_num)
#           print(' i=%d ' %(i))
           
            new = pd.DataFrame({'Ax':rabbo.Accx,'Ay':rabbo.Accy,'Az':rabbo.Accz,'Gx':rabbo.Gyrx,'Gy':rabbo.Gyry,'Gz':rabbo.Gyrz},index={i})
            df = df.append(new)
            time.sleep(0.1)
            i=i+1
            result.set("資料傳輸中...!!")
            if  i >1350:
                df.to_csv('./20210328test.csv')
                print('資料傳輸完畢!!')
                result.set("資料傳輸完畢!!")
                rabbo.stop()#停止運作
                break
            
    except  KeyboardInterrupt:#結束程式
        print('Shut done!')
        print (rabbo.Accx_list)#印出到結束程式時的所有 Accx 值
        df.to_csv('./20210328test.csv')
        print('資料傳輸完畢!!')
        rabbo.stop()#停止運作
    
root = tk.Tk()
root.title("人工智慧地震波形感測")
root.geometry("500x500")
#root.title('地震波形感測主視窗')
root.configure(bg='#FFFF93')

result = tk.StringVar()
result.set("波形資訊")

label1 = tk.Label(root,width=30,height=3,text="人工智慧地震波感測",font=("標楷體",20),bg='#FFFF93')
label1.pack()
label2 = tk.Label(root,width=30,height=3,textvariable=result,font=("標楷體",16),bg='#D3FF93',fg='#0000FF')
label2.pack()
#labe2 = tk.Label(root, text='bbb',bg='green')
#labe2.pack

button3 = tk.Button(root, text='地震波資料擷取',bg="#FFC9C9",width=30,height=3,font=("標楷體",16),command=start)
button3.pack()
button4 = tk.Button(root, text='AI-SVM',bg="#FFC9C9",width=30,height=3,font=("標楷體",16),command=SVM)
button4.pack()
button1 = tk.Button(root, text='地震波數據圖形分析',bg="#FFC9C9",width=30,height=3,font=("標楷體",16),command=analysis)
button1.pack()
button5 = tk.Button(root, text='地震波介紹影片',bg="#FFC9C9",width=30,height=3,font=("標楷體",16),command=video)
button5.pack()
root.mainloop()
