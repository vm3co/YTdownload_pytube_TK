import tkinter as tk
import tkinter.messagebox
import pytube as yt
from PIL import Image, ImageTk
import requests
from io import BytesIO
from tkinter import ttk

#===========================================
wiN = tk.Tk()
wiN.title("Youtube下載")
#計算螢幕大小將視窗置中顯示
wiNW = 1200
wiNH = 500
wiNL = int((wiN.winfo_screenwidth()-wiNW)/2)       # 計算左上 x 座標
wiNT = int((wiN.winfo_screenheight()-wiNH)/2)      # 計算左上 y 座標
wiN.geometry(f'{wiNW}x{wiNH}+{wiNL}+{wiNT}')
#固定視窗大小的作法
wiN.resizable(width=False, height=False)

#===========================================
#下載點網址
def _onProgress(stream, chunk, remains):
    total = stream.filesize                     # 取得完整尺寸
    percent = (total-remains) / total * 100     # 減去剩餘尺寸 ( 剩餘尺寸會抓取存取的檔案大小 )
    baR['value'] = percent
    vaLing.set(str(f"{percent:05.2f}")+" %")
    wiN1.update() 
   # print(f'下載中… {percent:05.2f}', end='\r')  # 顯示進度，\r 表示不換行，在同一行更新
    if percent == 100.0:
        wiN1.destroy()      
        
def _doW():
    global yT
    try:
        yT = yt.YouTube(entrY.get(), on_progress_callback=_onProgress)
        _show()
        _chO()
    except:
        tk.messagebox.showerror("錯誤","網址輸入錯誤!!")

frame1 = tk.Frame(wiN, height=200, width=700, bg='silver')   # 第一個 Frame 元件
frame1.place(relx=0, rely=0)   
titlE = tk.Label(frame1, text="Youtube下載", fg="black", bg="#FF9D6F", font=("標楷體",20,"bold"), width=50, pady=8)
titlE.place(x=0,y=0)
lbL1 = tk.Label(frame1,text="網址", fg="black", bg="#FF9D6F", font=("標楷體", 16), width=10, height=2)
lbL1.place(x=45,y=80)
entrY=tk.Entry(frame1,font=("Arial",16),bd=5,width=40)
entrY.place(x=175,y=85)
btN = tk.Button(frame1, text="送出!!", fg="black", bg="#9AFF02", font=("標楷體", 16), width=50, pady=5, command=_doW)
btN.place(x=80,y=140)

#===========================================
#影片類型
def _chO():
    raD1["state"]=tk.NORMAL
    raD2["state"]=tk.NORMAL
    raD3["state"]=tk.NORMAL
    btN21["state"]=tk.NORMAL

def _doW2():
    global nuMlisT
    nuMlisT=list()
    chOlisT=list()
    try:
        if vaL.get()=="mp4":
            streamS=list(yT.streams.filter(progressive=True))
            for ii in range(len(streamS)):
                ll=str(streamS[ii]).split('"')
                nuMlisT.append(ll[1])
                chOlisT.append(ll[5])
        elif vaL.get()=="mp3":
            streamS=list(yT.streams.filter(only_audio=True))
            for ii in range(len(streamS)):
                ll=str(streamS[ii]).split('"')
                nuMlisT.append(ll[1])
                chOlisT.append(ll[5])
        elif vaL.get()=="mp4x":
            streamS=list(yT.streams.filter(only_video=True))
            for ii in range(len(streamS)):
                ll=str(streamS[ii]).split('"')
                nuMlisT.append(ll[1])
                chOlisT.append(str(ll[3][6::])+" "+str(ll[5]))
        boX.delete(0,"end")
        for ii in chOlisT:
            boX.insert("end", ii)
        btN22["state"]=tk.NORMAL
    except yt.exceptions.LiveStreamError:
        tk.messagebox.showerror("錯誤","直播中無法下載!!")
    except:
        tk.messagebox.showerror("錯誤","此影片無法使用本程式下載!!")
        
def _no_closing():
    return
    
def _doW3():
    global wiN1,baR,vaLing
    qQ=tk.messagebox.askokcancel("提示","確定要下載嗎???")
    if qQ:
        wiN1=tk.Toplevel(wiN)
        wiN1.title("下載中...")
        wiN1W=220
        wiN1H=100
        wiN1L = int((wiN1.winfo_screenwidth() - wiN1W)/2)    # 取得螢幕寬度，計算左上 x 座標
        wiN1T = int((wiN1.winfo_screenheight() - wiN1H)/2)    # 取得螢幕高度，計算左上 y 座標
        wiN1.geometry(f"{wiN1W}x{wiN1H}+{wiN1L}+{wiN1T}")
        wiN1.resizable(width=False, height=False)
        wiN1.configure(bg='silver')     
        wiN1.protocol("WM_DELETE_WINDOW", _no_closing)        #使視窗無法按右上角關閉避免程式出錯

        baR = ttk.Progressbar(wiN1)
        baR.place(relx=0.28, rely=0.3)
        vaLing = tk.StringVar()
        lbL23 = tk.Label(wiN1, textvariable=vaLing, fg="black", bg="silver", font=("標楷體", 16,"bold"))
        lbL23.place(relx=0.3, rely=0.6)
        vaLing.set("0.0 %")
        
        n, = boX.curselection()
        nn=nuMlisT[n]
        yT.streams.get_by_itag(nn).download()
        tk.messagebox.showinfo("提示","下載完成!!!")

frame2 = tk.Frame(wiN,height=300, width=700, bg='#1AFD9C')   # 第二個 Frame 元件
frame2.place(relx=0, rely=0.4)   
#下載類型
lbL21 = tk.Label(frame2, text="下載類型", fg="black", bg="#1AFD9C", font=("標楷體", 16,"bold"), width=10, height=2)
lbL21.place(relx=0.06, rely=0.035)
vaL = tk.StringVar()  # 建立文字變數
raD1 = tk.Radiobutton(frame2, text='mp4',variable=vaL, value='mp4', fg="black", bg="#FF9D6F", font=("標楷體", 16), state=tk.DISABLED)      #mp4
raD1.place(relx=0.1, rely=0.25)
raD1.select()   # 選擇第一個 Radiobutton
raD2 = tk.Radiobutton(frame2, text='mp3',variable=vaL, value='mp3', fg="black", bg="#FF9D6F", font=("標楷體", 16), state=tk.DISABLED)      #mp3
raD2.place(relx=0.1, rely=0.45)
raD3 = tk.Radiobutton(frame2, text='無聲影像',variable=vaL, value='mp4x', fg="black", bg="#FF9D6F", font=("標楷體", 16), state=tk.DISABLED)      #mp3
raD3.place(relx=0.1, rely=0.65)
btN21 = tk.Button(frame2, text="確認下載類型", fg="black", bg="#FFA042", font=("標楷體", 16), width=15, pady=5, state=tk.DISABLED, command=_doW2)
btN21.place(relx=0.06, rely=0.8)
#解析度
lbL22 = tk.Label(frame2, text="解析度", fg="black", bg="#1AFD9C", font=("標楷體", 16,"bold"), width=10, height=2)
lbL22.place(relx=0.49, rely=0.03)
sBar=tk.Scrollbar(frame2)
boX=tk.Listbox(frame2, height=7, width=20, font=("Arial", 20),yscrollcommand=sBar.set)
sBar.place(in_=boX, relx=1.0, relheight=1.0)
boX.place(relx=0.35, rely=0.18)
sBar.config(command=boX.yview)
btN22 = tk.Button(frame2, text="開始下載", fg="black", bg="#FFA042", font=("標楷體", 16), width=8, pady=5, state=tk.DISABLED, command=_doW3)
btN22.place(relx=0.82, rely=0.45)

#===========================================
#影片名稱、長度、縮圖
def _show():
    hH = yT.length//60//60
    mM = yT.length//60-hH*60
    sS = yT.length%60
    if hH==0:
        yTtitlE=yT.title+"\n\n頻道："+yT.author+"\n時間長度:"+str(mM)+"分"+str(sS)+"秒"
    else:
        yTtitlE=yT.title+"\n\n頻道："+yT.author+"\n時間長度:"+str(hH)+"時"+str(mM)+"分"+str(sS)+"秒"
    lbL31["text"]=yTtitlE

    rS = requests.get(yT.thumbnail_url)
    imG = Image.open(BytesIO(rS.content)).resize((480,270)) # 開啟圖片並調整圖片大小
    tk_imG = ImageTk.PhotoImage(imG)                        # 轉換為 tk 圖片物件
    caN.delete('all')                                       # 清空 Canvas 原本內容
    caN.create_image(0, 0, anchor="nw", image=tk_imG)       # 建立圖片
    caN.image = tk_imG                                      # 修改屬性更新畫面

frame3 = tk.Frame(wiN, height=500, width=500, bg="#46A3FF")   # 第三個 Frame 元件
frame3.pack(side='right') 
lbL31 = tk.Label(frame3,text="", bg="#46A3FF", font=("標楷體", 16), wraplength=500, justify="left")
lbL31.place(relx=0, rely=0.05)
caN = tk.Canvas(frame3, width=480, height=270, bg="white")
caN.place(relx=0.02, rely=0.43)

#===========================================
wiN.mainloop()
