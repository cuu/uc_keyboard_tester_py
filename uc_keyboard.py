import evdev
import time
import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
from threading import Thread
import sys
from pynput.mouse import Listener,Button,Controller
from pynput import keyboard

joy_pathes = []
my_mouse = Controller()
threads = []
lastX = 0
lastY = 0
mouse_move = {}
joy_threads = []

class App:
    keys = {}
    joysticks = {}
    #hid = {}
    mouse = {}
    focusbg =  "#037bfc"
    normalbg = "#efefef"
    tip_label = None
    stage = 0
    marks = {}

    def clearAll(self):
        global mouse_move
        self.marks = {}
        for b in self.keys:
            btn = self.keys[b]
            btn["bg"] = self.normalbg

        for b in self.joysticks:
            btn = self.joysticks[b]
            btn["bg"] = self.normalbg

        for b in self.mouse:
            btn = self.mouse[b]
            btn["bg"] = self.normalbg

        mouse_move = {}
        self.stage = 0
        self.tipMsg("提示符")

    def tipMsg(self,msg):
        self.tip_label["text"] = msg 

    def assignKey(self,button):
        self.keys[button["text"]] = button
    
    def setMarks(self,m):
        self.marks[m] = 1
        #print(len(self.marks))
        if len(self.marks) == 68:
            self.stage = 2
            self.tipMsg("现在请按下 Fn + F1 完成本次测试")

    def greenMouseLabel(self,idx):
        if idx in self.mouse:
            b = self.mouse[idx]
            b["bg"] = self.focusbg
            self.setMarks(idx)

    def greenJoystickLabel(self,idx):
        if idx  in self.joysticks:
            b = self.joysticks[idx]
            b["bg"] = self.focusbg
            self.setMarks(idx)

    def greenKeyboardLabel(self,idx):
        #print(idx)
        if idx.lower().capitalize() in self.keys:
            b = self.keys[idx.lower().capitalize()]
            b["bg"] = self.focusbg
            self.setMarks(idx.lower().capitalize())

    def __init__(self, root):
        #setting title
        root.title("keyboard tester")
        #setting window size
        width=699
        height=480
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        root.update()
        # 获取窗口大小和位置        
        geo = root.geometry()
        #print(geo)  # 例如"500x300+200+150"
        # 分割字符串获取x和y坐标
        parts = geo.split('+')
        x = int(parts[1])  
        y = int(parts[2])  
        #print(root.winfo_width(),root.winfo_height())
        # 求窗口中间位置  
        mid_x = x + root.winfo_width() / 2   
        mid_y = y + root.winfo_height() / 2 

        # 移动鼠标 
        my_mouse.position = (mid_x, mid_y)  

        GButton_138=tk.Button(root)
        GButton_138["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_138["font"] = ft
        GButton_138["fg"] = "#000000"
        GButton_138["justify"] = "center"
        GButton_138["text"] = "⯅"
        GButton_138.place(x=80,y=30,width=30,height=30)
        GButton_138["command"] = self.GButton_138_command

        self.keys["Up"] =  GButton_138

        GButton_96=tk.Button(root)
        GButton_96["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_96["font"] = ft
        GButton_96["fg"] = "#000000"
        GButton_96["justify"] = "center"
        GButton_96["text"] = "⯇"
        GButton_96.place(x=50,y=60,width=30,height=30)
        GButton_96["command"] = self.GButton_96_command
        self.keys["Left"] = GButton_96

        GButton_492=tk.Button(root)
        GButton_492["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_492["font"] = ft
        GButton_492["fg"] = "#000000"
        GButton_492["justify"] = "center"
        GButton_492["text"] = "⯈"
        GButton_492.place(x=110,y=60,width=30,height=30)
        GButton_492["command"] = self.GButton_492_command
        self.keys["Right"] = GButton_492

        GButton_125=tk.Button(root)
        GButton_125["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_125["font"] = ft
        GButton_125["fg"] = "#000000"
        GButton_125["justify"] = "center"
        GButton_125["text"] = "⯆"
        GButton_125.place(x=80,y=90,width=30,height=30)
        GButton_125["command"] = self.GButton_125_command
        self.keys["Down"] = GButton_125

        GButton_805=tk.Button(root)
        GButton_805["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_805["font"] = ft
        GButton_805["fg"] = "#000000"
        GButton_805["justify"] = "center"
        GButton_805["text"] = "Select"
        GButton_805.place(x=140,y=130,width=46,height=30)
        GButton_805["command"] = self.GButton_805_command
        self.joysticks["Select"] = GButton_805

        GButton_303=tk.Button(root)
        GButton_303["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_303["font"] = ft
        GButton_303["fg"] = "#000000"
        GButton_303["justify"] = "center"
        GButton_303["text"] = "Start"
        GButton_303.place(x=190,y=130,width=46,height=30)
        GButton_303["command"] = self.GButton_303_command
        self.joysticks["Start"] = GButton_303

        GButton_446=tk.Button(root)
        GButton_446["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_446["font"] = ft
        GButton_446["fg"] = "#000000"
        GButton_446["justify"] = "center"
        GButton_446["text"] = "Vol"
        GButton_446.place(x=310,y=130,width=30,height=30)
        GButton_446["command"] = self.GButton_446_command
        self.keys["Media_volume_down"] = GButton_446

        GButton_244=tk.Button(root)
        GButton_244["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_244["font"] = ft
        GButton_244["fg"] = "#000000"
        GButton_244["justify"] = "center"
        GButton_244["text"] = "~"
        GButton_244.place(x=90,y=170,width=30,height=30)
        GButton_244["command"] = self.GButton_244_command
        self.keys["`"] = GButton_244


        GButton_934=tk.Button(root)
        GButton_934["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_934["font"] = ft
        GButton_934["fg"] = "#000000"
        GButton_934["justify"] = "center"
        GButton_934["text"] = "轨迹球"
        GButton_934.place(x=450,y=50,width=44,height=44)
        GButton_934["command"] = self.GButton_934_command

        self.keys["Trackball"] = GButton_934

        GButton_830=tk.Button(root)
        GButton_830["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_830["font"] = ft
        GButton_830["fg"] = "#000000"
        GButton_830["justify"] = "center"
        GButton_830["text"] = "["
        GButton_830.place(x=350,y=130,width=30,height=30)
        GButton_830["command"] = self.GButton_830_command
        self.assignKey(GButton_830)

        GButton_692=tk.Button(root)
        GButton_692["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_692["font"] = ft
        GButton_692["fg"] = "#000000"
        GButton_692["justify"] = "center"
        GButton_692["text"] = "]"
        GButton_692.place(x=390,y=130,width=31,height=30)
        GButton_692["command"] = self.GButton_692_command
        self.assignKey(GButton_692)


        GButton_729=tk.Button(root)
        GButton_729["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_729["font"] = ft
        GButton_729["fg"] = "#000000"
        GButton_729["justify"] = "center"
        GButton_729["text"] = "="
        GButton_729.place(x=510,y=130,width=30,height=30)
        GButton_729["command"] = self.GButton_729_command
        self.assignKey(GButton_729)

        GButton_860=tk.Button(root)
        GButton_860["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_860["font"] = ft
        GButton_860["fg"] = "#000000"
        GButton_860["justify"] = "center"
        GButton_860["text"] = "X"
        GButton_860.place(x=570,y=30,width=30,height=30)
        GButton_860["command"] = self.GButton_860_command
        self.joysticks["X"] =  GButton_860

        GButton_473=tk.Button(root)
        GButton_473["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_473["font"] = ft
        GButton_473["fg"] = "#000000"
        GButton_473["justify"] = "center"
        GButton_473["text"] = "Y"
        GButton_473.place(x=530,y=30,width=30,height=30)
        GButton_473["command"] = self.GButton_473_command

        self.joysticks["Y"] = GButton_473

        GButton_557=tk.Button(root)
        GButton_557["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_557["font"] = ft
        GButton_557["fg"] = "#000000"
        GButton_557["justify"] = "center"
        GButton_557["text"] = "B"
        GButton_557.place(x=540,y=70,width=30,height=30)
        GButton_557["command"] = self.GButton_557_command

        self.joysticks["B"] = GButton_557

        GButton_149=tk.Button(root)
        GButton_149["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_149["font"] = ft
        GButton_149["fg"] = "#000000"
        GButton_149["justify"] = "center"
        GButton_149["text"] = "1"
        GButton_149.place(x=130,y=170,width=30,height=30)
        GButton_149["command"] = self.GButton_149_command

        self.assignKey(GButton_149)

        GButton_950=tk.Button(root)
        GButton_950["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_950["font"] = ft
        GButton_950["fg"] = "#000000"
        GButton_950["justify"] = "center"
        GButton_950["text"] = "2"
        GButton_950.place(x=170,y=170,width=30,height=30)
        GButton_950["command"] = self.GButton_950_command

        self.assignKey(GButton_950)

        GButton_664=tk.Button(root)
        GButton_664["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_664["font"] = ft
        GButton_664["fg"] = "#000000"
        GButton_664["justify"] = "center"
        GButton_664["text"] = "4"
        GButton_664.place(x=250,y=170,width=30,height=30)
        GButton_664["command"] = self.GButton_664_command

        self.assignKey(GButton_664)

        GButton_624=tk.Button(root)
        GButton_624["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_624["font"] = ft
        GButton_624["fg"] = "#000000"
        GButton_624["justify"] = "center"
        GButton_624["text"] = "5"
        GButton_624.place(x=290,y=170,width=30,height=30)
        GButton_624["command"] = self.GButton_624_command

        self.assignKey(GButton_624)

        GButton_875=tk.Button(root)
        GButton_875["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_875["font"] = ft
        GButton_875["fg"] = "#000000"
        GButton_875["justify"] = "center"
        GButton_875["text"] = "6"
        GButton_875.place(x=330,y=170,width=30,height=30)
        GButton_875["command"] = self.GButton_875_command

        self.assignKey(GButton_875)

        GButton_9=tk.Button(root)
        GButton_9["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_9["font"] = ft
        GButton_9["fg"] = "#000000"
        GButton_9["justify"] = "center"
        GButton_9["text"] = "8"
        GButton_9.place(x=410,y=170,width=30,height=30)
        GButton_9["command"] = self.GButton_9_command

        self.assignKey(GButton_9)

        GButton_990=tk.Button(root)
        GButton_990["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_990["font"] = ft
        GButton_990["fg"] = "#000000"
        GButton_990["justify"] = "center"
        GButton_990["text"] = "9"
        GButton_990.place(x=450,y=170,width=30,height=30)
        GButton_990["command"] = self.GButton_990_command

        self.assignKey(GButton_990)

        GButton_162=tk.Button(root)
        GButton_162["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_162["font"] = ft
        GButton_162["fg"] = "#000000"
        GButton_162["justify"] = "center"
        GButton_162["text"] = "0"
        GButton_162.place(x=490,y=170,width=30,height=30)
        GButton_162["command"] = self.GButton_162_command

        self.assignKey(GButton_162)

        GButton_818=tk.Button(root)
        GButton_818["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_818["font"] = ft
        GButton_818["fg"] = "#000000"
        GButton_818["justify"] = "center"
        GButton_818["text"] = "Esc"
        GButton_818.place(x=80,y=130,width=54,height=30)
        GButton_818["command"] = self.GButton_818_command

        self.assignKey(GButton_818)

        GButton_841=tk.Button(root)
        GButton_841["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_841["font"] = ft
        GButton_841["fg"] = "#000000"
        GButton_841["justify"] = "center"
        GButton_841["text"] = "Q"
        GButton_841.place(x=110,y=210,width=30,height=30)
        GButton_841["command"] = self.GButton_841_command

        self.assignKey(GButton_841)

        GButton_584=tk.Button(root)
        GButton_584["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_584["font"] = ft
        GButton_584["fg"] = "#000000"
        GButton_584["justify"] = "center"
        GButton_584["text"] = "W"
        GButton_584.place(x=150,y=210,width=30,height=30)
        GButton_584["command"] = self.GButton_584_command

        self.assignKey(GButton_584)

        GButton_421=tk.Button(root)
        GButton_421["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_421["font"] = ft
        GButton_421["fg"] = "#000000"
        GButton_421["justify"] = "center"
        GButton_421["text"] = "E"
        GButton_421.place(x=190,y=210,width=30,height=30)
        GButton_421["command"] = self.GButton_421_command

        self.assignKey(GButton_421)

        GButton_694=tk.Button(root)
        GButton_694["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_694["font"] = ft
        GButton_694["fg"] = "#000000"
        GButton_694["justify"] = "center"
        GButton_694["text"] = "R"
        GButton_694.place(x=230,y=210,width=30,height=30)
        GButton_694["command"] = self.GButton_694_command

        self.assignKey(GButton_694)

        GButton_966=tk.Button(root)
        GButton_966["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_966["font"] = ft
        GButton_966["fg"] = "#000000"
        GButton_966["justify"] = "center"
        GButton_966["text"] = "T"
        GButton_966.place(x=270,y=210,width=30,height=30)
        GButton_966["command"] = self.GButton_966_command

        self.assignKey(GButton_966)

        GButton_587=tk.Button(root)
        GButton_587["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_587["font"] = ft
        GButton_587["fg"] = "#000000"
        GButton_587["justify"] = "center"
        GButton_587["text"] = "Y"
        GButton_587.place(x=310,y=210,width=30,height=30)
        GButton_587["command"] = self.GButton_587_command

        self.assignKey(GButton_587)

        GButton_871=tk.Button(root)
        GButton_871["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_871["font"] = ft
        GButton_871["fg"] = "#000000"
        GButton_871["justify"] = "center"
        GButton_871["text"] = "U"
        GButton_871.place(x=350,y=210,width=30,height=30)
        GButton_871["command"] = self.GButton_871_command

        self.assignKey(GButton_871)

        GButton_211=tk.Button(root)
        GButton_211["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_211["font"] = ft
        GButton_211["fg"] = "#000000"
        GButton_211["justify"] = "center"
        GButton_211["text"] = "I"
        GButton_211.place(x=390,y=210,width=30,height=30)
        GButton_211["command"] = self.GButton_211_command

        self.assignKey(GButton_211)

        GButton_89=tk.Button(root)
        GButton_89["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_89["font"] = ft
        GButton_89["fg"] = "#000000"
        GButton_89["justify"] = "center"
        GButton_89["text"] = "O"
        GButton_89.place(x=430,y=210,width=30,height=30)
        GButton_89["command"] = self.GButton_89_command

        self.assignKey(GButton_89)

        GButton_407=tk.Button(root)
        GButton_407["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_407["font"] = ft
        GButton_407["fg"] = "#000000"
        GButton_407["justify"] = "center"
        GButton_407["text"] = "P"
        GButton_407.place(x=470,y=210,width=30,height=30)
        GButton_407["command"] = self.GButton_407_command

        self.assignKey(GButton_407)

        GButton_28=tk.Button(root)
        GButton_28["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_28["font"] = ft
        GButton_28["fg"] = "#000000"
        GButton_28["justify"] = "center"
        GButton_28["text"] = "\\"
        GButton_28.place(x=550,y=130,width=30,height=30)
        GButton_28["command"] = self.GButton_28_command
        
        self.keys["Double_slash"] = GButton_28

        GButton_997=tk.Button(root)
        GButton_997["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_997["font"] = ft
        GButton_997["fg"] = "#000000"
        GButton_997["justify"] = "center"
        GButton_997["text"] = "Backspace"
        GButton_997.place(x=530,y=170,width=68,height=30)
        GButton_997["command"] = self.GButton_997_command
        
        self.assignKey(GButton_997)

        GButton_690=tk.Button(root)
        GButton_690["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_690["font"] = ft
        GButton_690["fg"] = "#000000"
        GButton_690["justify"] = "center"
        GButton_690["text"] = "Tab"
        GButton_690.place(x=60,y=210,width=44,height=30)
        GButton_690["command"] = self.GButton_690_command

        self.keys["Tab"] = GButton_690

        GButton_714=tk.Button(root)
        GButton_714["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_714["font"] = ft
        GButton_714["fg"] = "#000000"
        GButton_714["justify"] = "center"
        GButton_714["text"] = "A"
        GButton_714.place(x=120,y=250,width=30,height=30)
        GButton_714["command"] = self.GButton_714_command

        self.assignKey(GButton_714)

        GButton_672=tk.Button(root)
        GButton_672["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_672["font"] = ft
        GButton_672["fg"] = "#000000"
        GButton_672["justify"] = "center"
        GButton_672["text"] = "S"
        GButton_672.place(x=160,y=250,width=30,height=30)
        GButton_672["command"] = self.GButton_672_command

        self.assignKey(GButton_672)

        GButton_877=tk.Button(root)
        GButton_877["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_877["font"] = ft
        GButton_877["fg"] = "#000000"
        GButton_877["justify"] = "center"
        GButton_877["text"] = "D"
        GButton_877.place(x=200,y=250,width=30,height=30)
        GButton_877["command"] = self.GButton_877_command

        self.assignKey(GButton_877)

        GButton_747=tk.Button(root)
        GButton_747["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_747["font"] = ft
        GButton_747["fg"] = "#000000"
        GButton_747["justify"] = "center"
        GButton_747["text"] = "G"
        GButton_747.place(x=280,y=250,width=30,height=30)
        GButton_747["command"] = self.GButton_747_command

        self.assignKey(GButton_747)

        GButton_878=tk.Button(root)
        GButton_878["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_878["font"] = ft
        GButton_878["fg"] = "#000000"
        GButton_878["justify"] = "center"
        GButton_878["text"] = "J"
        GButton_878.place(x=360,y=250,width=30,height=30)
        GButton_878["command"] = self.GButton_878_command

        self.assignKey(GButton_878)

        GButton_386=tk.Button(root)
        GButton_386["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_386["font"] = ft
        GButton_386["fg"] = "#000000"
        GButton_386["justify"] = "center"
        GButton_386["text"] = "K"
        GButton_386.place(x=400,y=250,width=30,height=30)
        GButton_386["command"] = self.GButton_386_command

        self.assignKey(GButton_386)

        GButton_115=tk.Button(root)
        GButton_115["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_115["font"] = ft
        GButton_115["fg"] = "#000000"
        GButton_115["justify"] = "center"
        GButton_115["text"] = "L"
        GButton_115.place(x=440,y=250,width=30,height=30)
        GButton_115["command"] = self.GButton_115_command

        self.assignKey(GButton_115)

        GButton_611=tk.Button(root)
        GButton_611["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_611["font"] = ft
        GButton_611["fg"] = "#000000"
        GButton_611["justify"] = "center"
        GButton_611["text"] = ";"
        GButton_611.place(x=480,y=250,width=30,height=30)
        GButton_611["command"] = self.GButton_611_command

        self.assignKey(GButton_611)

        GButton_229=tk.Button(root)
        GButton_229["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_229["font"] = ft
        GButton_229["fg"] = "#000000"
        GButton_229["justify"] = "center"
        GButton_229["text"] = "'"
        GButton_229.place(x=80,y=250,width=30,height=30)
        GButton_229["command"] = self.GButton_229_command

        self.keys["Sig_dot"] = GButton_229 

        GButton_59=tk.Button(root)
        GButton_59["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_59["font"] = ft
        GButton_59["fg"] = "#000000"
        GButton_59["justify"] = "center"
        GButton_59["text"] = "Shift"
        GButton_59.place(x=60,y=290,width=57,height=30)
        GButton_59["command"] = self.GButton_59_command

        self.assignKey(GButton_59)

        GButton_455=tk.Button(root)
        GButton_455["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_455["font"] = ft
        GButton_455["fg"] = "#000000"
        GButton_455["justify"] = "center"
        GButton_455["text"] = "Z"
        GButton_455.place(x=130,y=290,width=30,height=30)
        GButton_455["command"] = self.GButton_455_command

        self.assignKey(GButton_455)

        GButton_54=tk.Button(root)
        GButton_54["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_54["font"] = ft
        GButton_54["fg"] = "#000000"
        GButton_54["justify"] = "center"
        GButton_54["text"] = "X"
        GButton_54.place(x=170,y=290,width=30,height=30)
        GButton_54["command"] = self.GButton_54_command

        self.assignKey(GButton_54)

        GButton_777=tk.Button(root)
        GButton_777["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_777["font"] = ft
        GButton_777["fg"] = "#000000"
        GButton_777["justify"] = "center"
        GButton_777["text"] = "C"
        GButton_777.place(x=210,y=290,width=30,height=30)
        GButton_777["command"] = self.GButton_777_command

        self.assignKey(GButton_777)

        GButton_893=tk.Button(root)
        GButton_893["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_893["font"] = ft
        GButton_893["fg"] = "#000000"
        GButton_893["justify"] = "center"
        GButton_893["text"] = "V"
        GButton_893.place(x=250,y=290,width=30,height=30)
        GButton_893["command"] = self.GButton_893_command

        self.assignKey(GButton_893)

        GButton_300=tk.Button(root)
        GButton_300["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_300["font"] = ft
        GButton_300["fg"] = "#000000"
        GButton_300["justify"] = "center"
        GButton_300["text"] = "B"
        GButton_300.place(x=290,y=290,width=30,height=30)
        GButton_300["command"] = self.GButton_300_command

        self.assignKey(GButton_300)

        GButton_651=tk.Button(root)
        GButton_651["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_651["font"] = ft
        GButton_651["fg"] = "#000000"
        GButton_651["justify"] = "center"
        GButton_651["text"] = "N"
        GButton_651.place(x=330,y=290,width=30,height=30)
        GButton_651["command"] = self.GButton_651_command

        self.assignKey(GButton_651)

        GButton_239=tk.Button(root)
        GButton_239["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_239["font"] = ft
        GButton_239["fg"] = "#000000"
        GButton_239["justify"] = "center"
        GButton_239["text"] = "M"
        GButton_239.place(x=370,y=290,width=30,height=30)
        GButton_239["command"] = self.GButton_239_command

        self.assignKey(GButton_239)

        GButton_399=tk.Button(root)
        GButton_399["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_399["font"] = ft
        GButton_399["fg"] = "#000000"
        GButton_399["justify"] = "center"
        GButton_399["text"] = "<"
        GButton_399.place(x=410,y=290,width=30,height=30)
        GButton_399["command"] = self.GButton_399_command
        
        self.keys[","] = GButton_399

        GButton_582=tk.Button(root)
        GButton_582["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_582["font"] = ft
        GButton_582["fg"] = "#000000"
        GButton_582["justify"] = "center"
        GButton_582["text"] = ">"
        GButton_582.place(x=450,y=290,width=30,height=30)
        GButton_582["command"] = self.GButton_582_command

        self.keys["."] = GButton_582

        GButton_635=tk.Button(root)
        GButton_635["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_635["font"] = ft
        GButton_635["fg"] = "#000000"
        GButton_635["justify"] = "center"
        GButton_635["text"] = "/"
        GButton_635.place(x=430,y=130,width=30,height=30)
        GButton_635["command"] = self.GButton_635_command

        self.assignKey(GButton_635)

        GButton_401=tk.Button(root)
        GButton_401["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_401["font"] = ft
        GButton_401["fg"] = "#000000"
        GButton_401["justify"] = "center"
        GButton_401["text"] = "Shift"
        GButton_401.place(x=490,y=290,width=49,height=30)
        GButton_401["command"] = self.GButton_401_command

        self.keys["Shift_r"] = GButton_401

        GButton_994=tk.Button(root)
        GButton_994["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_994["font"] = ft
        GButton_994["fg"] = "#000000"
        GButton_994["justify"] = "center"
        GButton_994["text"] = "Fn"
        GButton_994.place(x=90,y=330,width=30,height=30)
        GButton_994["command"] = self.GButton_994_command

        GButton_420=tk.Button(root)
        GButton_420["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_420["font"] = ft
        GButton_420["fg"] = "#000000"
        GButton_420["justify"] = "center"
        GButton_420["text"] = "Alt"
        GButton_420.place(x=170,y=330,width=30,height=30)
        GButton_420["command"] = self.GButton_420_command

        self.assignKey(GButton_420)

        GButton_454=tk.Button(root)
        GButton_454["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_454["font"] = ft
        GButton_454["fg"] = "#000000"
        GButton_454["justify"] = "center"
        GButton_454["text"] = "Space"
        GButton_454.place(x=210,y=330,width=191,height=30)
        GButton_454["command"] = self.GButton_454_command

        self.assignKey(GButton_454)

        GButton_324=tk.Button(root)
        GButton_324["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_324["font"] = ft
        GButton_324["fg"] = "#000000"
        GButton_324["justify"] = "center"
        GButton_324["text"] = "Alt"
        GButton_324.place(x=410,y=330,width=30,height=30)
        GButton_324["command"] = self.GButton_324_command
        self.keys["Alt_r"] = GButton_324

        GButton_42=tk.Button(root)
        GButton_42["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_42["font"] = ft
        GButton_42["fg"] = "#000000"
        GButton_42["justify"] = "center"
        GButton_42["text"] = "Ctrl"
        GButton_42.place(x=450,y=330,width=30,height=30)
        GButton_42["command"] = self.GButton_42_command
        self.keys["Ctrl_r"]= GButton_42

        GButton_921=tk.Button(root)
        GButton_921["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_921["font"] = ft
        GButton_921["fg"] = "#000000"
        GButton_921["justify"] = "center"
        GButton_921["text"] = "-"
        GButton_921.place(x=470,y=130,width=30,height=30)
        GButton_921["command"] = self.GButton_921_command

        self.assignKey(GButton_921)

        GButton_788=tk.Button(root)
        GButton_788["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_788["font"] = ft
        GButton_788["fg"] = "#000000"
        GButton_788["justify"] = "center"
        GButton_788["text"] = "3"
        GButton_788.place(x=210,y=170,width=30,height=30)
        GButton_788["command"] = self.GButton_788_command

        self.assignKey(GButton_788)

        GButton_909=tk.Button(root)
        GButton_909["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_909["font"] = ft
        GButton_909["fg"] = "#000000"
        GButton_909["justify"] = "center"
        GButton_909["text"] = "7"
        GButton_909.place(x=370,y=170,width=30,height=30)
        GButton_909["command"] = self.GButton_909_command

        self.assignKey(GButton_909)

        GButton_696=tk.Button(root)
        GButton_696["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_696["font"] = ft
        GButton_696["fg"] = "#000000"
        GButton_696["justify"] = "center"
        GButton_696["text"] = "A"
        GButton_696.place(x=580,y=70,width=30,height=30)
        GButton_696["command"] = self.GButton_696_command

        self.joysticks["A"] = GButton_696

        GLabel_975=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_975["font"] = ft
        GLabel_975["fg"] = "#333333"
        GLabel_975["justify"] = "center"
        GLabel_975["text"] = "提示符"
        GLabel_975.place(x=210,y=20,width=236,height=96)
        
        self.tip_label = GLabel_975

        GButton_550=tk.Button(root)
        GButton_550["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_550["font"] = ft
        GButton_550["fg"] = "#000000"
        GButton_550["justify"] = "center"
        GButton_550["text"] = "重置测试"
        GButton_550.place(x=620,y=350,width=64,height=45)
        GButton_550["command"] = self.GButton_550_command

        GButton_680=tk.Button(root)
        GButton_680["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_680["font"] = ft
        GButton_680["fg"] = "#000000"
        GButton_680["justify"] = "center"
        GButton_680["text"] = "L"
        GButton_680.place(x=160,y=30,width=30,height=30)
        GButton_680["command"] = self.GButton_680_command

        self.mouse["left"] = GButton_680

        GButton_495=tk.Button(root)
        GButton_495["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_495["font"] = ft
        GButton_495["fg"] = "#000000"
        GButton_495["justify"] = "center"
        GButton_495["text"] = "R"
        GButton_495.place(x=180,y=70,width=30,height=30)
        GButton_495["command"] = self.GButton_495_command

        self.mouse["right"] = GButton_495

        GButton_612=tk.Button(root)
        GButton_612["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_612["font"] = ft
        GButton_612["fg"] = "#000000"
        GButton_612["justify"] = "center"
        GButton_612["text"] = "Enter"
        GButton_612.place(x=520,y=250,width=70,height=30)
        GButton_612["command"] = self.GButton_612_command

        self.assignKey(GButton_612)

        GButton_588=tk.Button(root)
        GButton_588["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_588["font"] = ft
        GButton_588["fg"] = "#000000"
        GButton_588["justify"] = "center"
        GButton_588["text"] = "Fn"
        GButton_588.place(x=490,y=330,width=30,height=30)
        GButton_588["command"] = self.GButton_588_command

        GButton_865=tk.Button(root)
        GButton_865["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_865["font"] = ft
        GButton_865["fg"] = "#000000"
        GButton_865["justify"] = "center"
        GButton_865["text"] = "F"
        GButton_865.place(x=240,y=250,width=30,height=30)
        GButton_865["command"] = self.GButton_865_command

        self.assignKey(GButton_865)

        GButton_358=tk.Button(root)
        GButton_358["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_358["font"] = ft
        GButton_358["fg"] = "#000000"
        GButton_358["justify"] = "center"
        GButton_358["text"] = "H"
        GButton_358.place(x=320,y=250,width=30,height=30)
        GButton_358["command"] = self.GButton_358_command

        self.assignKey(GButton_358)

        GButton_822=tk.Button(root)
        GButton_822["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_822["font"] = ft
        GButton_822["fg"] = "#000000"
        GButton_822["justify"] = "center"
        GButton_822["text"] = "Ctrl"
        GButton_822.place(x=130,y=330,width=30,height=30)
        GButton_822["command"] = self.GButton_822_command

        self.assignKey(GButton_822)

    def GButton_550_command(self):
        self.clearAll()

    def GButton_138_command(self):
        print("command")


    def GButton_96_command(self):
        print("command")


    def GButton_492_command(self):
        print("command")


    def GButton_125_command(self):
        print("command")


    def GButton_805_command(self):
        print("command")


    def GButton_303_command(self):
        print("command")


    def GButton_446_command(self):
        print("command")


    def GButton_244_command(self):
        print("command")


    def GButton_934_command(self):
        print("command")


    def GButton_830_command(self):
        print("command")


    def GButton_692_command(self):
        print("command")


    def GButton_729_command(self):
        print("command")


    def GButton_860_command(self):
        print("command")


    def GButton_473_command(self):
        print("command")


    def GButton_557_command(self):
        print("command")


    def GButton_149_command(self):
        print("command")


    def GButton_950_command(self):
        print("command")


    def GButton_664_command(self):
        print("command")


    def GButton_624_command(self):
        print("command")


    def GButton_875_command(self):
        print("command")


    def GButton_9_command(self):
        print("command")


    def GButton_990_command(self):
        print("command")


    def GButton_162_command(self):
        print("command")


    def GButton_818_command(self):
        print("command")


    def GButton_841_command(self):
        print("command")


    def GButton_584_command(self):
        print("command")


    def GButton_421_command(self):
        print("command")


    def GButton_694_command(self):
        print("command")


    def GButton_966_command(self):
        print("command")


    def GButton_587_command(self):
        print("command")


    def GButton_871_command(self):
        print("command")


    def GButton_211_command(self):
        print("command")


    def GButton_89_command(self):
        print("command")


    def GButton_407_command(self):
        print("command")


    def GButton_28_command(self):
        print("command")


    def GButton_997_command(self):
        print("command")


    def GButton_690_command(self):
        print("command")


    def GButton_714_command(self):
        print("command")


    def GButton_672_command(self):
        print("command")


    def GButton_877_command(self):
        print("command")


    def GButton_747_command(self):
        print("command")


    def GButton_878_command(self):
        print("command")


    def GButton_386_command(self):
        print("command")


    def GButton_115_command(self):
        print("command")


    def GButton_611_command(self):
        print("command")


    def GButton_229_command(self):
        print("command")


    def GButton_59_command(self):
        print("command")


    def GButton_455_command(self):
        print("command")


    def GButton_54_command(self):
        print("command")


    def GButton_777_command(self):
        print("command")


    def GButton_893_command(self):
        print("command")


    def GButton_300_command(self):
        print("command")


    def GButton_651_command(self):
        print("command")


    def GButton_239_command(self):
        print("command")


    def GButton_399_command(self):
        print("command")


    def GButton_582_command(self):
        print("command")


    def GButton_635_command(self):
        print("command")


    def GButton_401_command(self):
        print("command")


    def GButton_994_command(self):
        print("command")


    def GButton_420_command(self):
        print("command")


    def GButton_454_command(self):
        print("command")


    def GButton_324_command(self):
        print("command")


    def GButton_42_command(self):
        print("command")


    def GButton_415_command(self):
        print("command")


    def GButton_267_command(self):
        print("command")


    def GButton_921_command(self):
        print("command")


    def GButton_788_command(self):
        print("command")


    def GButton_909_command(self):
        print("command")


    def GButton_696_command(self):
        print("command")

    def GButton_680_command(self):
        print("command")


    def GButton_495_command(self):
        print("command")


    def GButton_612_command(self):
        print("command")


    def GButton_588_command(self):
        print("command")


    def GButton_865_command(self):
        print("command")


    def GButton_358_command(self):
        print("command")


    def GButton_822_command(self):
        print("command")


    def GButton_759_command(self):
        print("command")

def on_move(x, y):
    global lastX,lastY

    effDis = 30
    if lastX < x and  x - lastX > effDis:
        mouse_move["right"] = 1

    if lastX > x and lastX - x > effDis:
        mouse_move["left"] = 1

    if lastY < y and y - lastY > effDis:
        mouse_move["down"] = 1

    if lastY > y and lastY - y > effDis:
        mouse_move["up"] = 1

    if "right" in mouse_move and "left" in mouse_move and "down" in mouse_move and "up" in mouse_move:
        app.greenKeyboardLabel("trackball")

    lastX = x
    lastY = y

def on_click(x, y, button, pressed):
    global app
    if pressed == True:
        if button == Button.left:
            app.greenMouseLabel("left")
        if button == Button.right:
            app.greenMouseLabel("right")
        if button == Button.middle:
            app.greenMouseLabel("middle")

def on_scroll(x,y,dx,dy):
    pass

def mouseListenThread(app):
    with Listener(on_move=on_move, on_click=on_click) as listener:
        try:
            listener.join()
        except Exception as e:
            print("mouse listen errors: ",e)

def on_press(key):
    print(key)
    key_str = str(key)
    key_str = key_str.replace("Key.","")
    if "\\" in key_str:
        print("double")
        key_str = "Double_slash"

    if key_str.count("'") == 1:
        print("single dot")
        key_str = "sig_dot"
    
    if key_str.count("'") > 1:
        key_str = key_str.replace("'","")

    if key_str =="f1":
        if app.stage == 2:
            messagebox.showinfo('提醒', '本次测试成功完成 PASSED')
            app.clearAll()
    else:
        app.greenKeyboardLabel(key_str)

def keyboardListenThread(app):
    with keyboard.Listener(
        on_press=on_press) as listener:
        try:
            listener.join()
        except Exception as e:
            print('{0} was pressed'.format(e.args[0]))

        # Wait for the next event.
        #event = keyboard.read_event()
        #if event.event_type == "down":
        #    event_name = event.name
        #    if event.scan_code == 42 or event.scan_code == 97 or event.scan_code == 100:
        #        event_name = "r"+event.name
        #    if event.scan_code == 54 or event.scan_code == 56 or event.scan_code == 29:
        #        event_name = "l"+event.name
        #    if event.scan_code == 126:
        #        event_name = "cmd"

        #   app.greenKeyboardLabel(event_name)

        #   print(event.event_type, event.name,event.scan_code,event.modifiers)

def searchJoystickOnce():
    global joy_threads
    global joy_pathes

    loop = True 
    found = False
    
    app.tipMsg("搜索设备中...")
    for t in joy_threads:
        if t.is_alive == True:
            t.terminate()
    joy_threads = [] 
    joy_pathes = []

    devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
    for device in devices:
        wholeName = device.name +device.phys
        print(wholeName)
        if "ClockworkPI DevTermusb" in wholeName:
            print(device.path , "joystick")
            joy_pathes.append(device.path)
    
    if len(joy_pathes) > 0:
        app.tipMsg("发现设备")

    startJoystickListen()

def searchJoystick():
    global joy_threads
    loop = True
    found = False

    for t in joy_threads:
        if t.is_alive == True:
            t.terminate()
    joy_threads = []

    while loop:
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        found = False
        for device in devices:
            wholeName = device.name +device.phys
            print(wholeName)
            if "ClockworkPI uConsoleusb" in wholeName:
                print(device.path , "joystick")
                joy_pathes.append(device.path)
                found = True

        startJoystickListen()
        
        if found == True:
            app.tipMsg("键盘已经连接，请测试")
            loop = False
        else:
            time.sleep(0.5)
    
    print("searchJoyStick done")
    return

joystick_type1map = {288:"X",289:"A",290:"B",291:"Y",296:"Select",297:"Start"}
joystick_type2map = {0:"x",1:"y"}

def listenPath(p):
    device = evdev.InputDevice(p)
    print("listenPath: ",device)
    try:
        for event in device.read_loop():
            t = event.type
            if int(t) == 1:
                if int(event.code) in joystick_type1map:
                    app.greenJoystickLabel( joystick_type1map[int(event.code)])
                    print(event)
            if int(t) == 3:#arrow
                if int(event.code) in joystick_type2map:
                    print("in type2map",event)
                    labelA = joystick_type2map[int(event.code)]
                    labelB = ""
                    if int(event.value) > 1000:
                        labelB = "10"
                    if int(event.value) == 0:
                        labelB = "-10"

                    print( labelA + labelB)
                    app.greenJoystickLabel(labelA + labelB)

    except Exception as e:
        print(e)
        app.clearAll()
        app.tipMsg("键盘被拔出，等待重新接入")
        joy_pathes.remove(p)
        print(joy_pathes) 
        Thread(target=searchJoystick).start()
    return

def startJoystickListen():
    global joy_threads
    global joy_pathes
    for j_p in joy_pathes:
        t = Thread(target=listenPath, args=(j_p,))
        #threads.append(t)
        #for th in threads:
        #    print("thread isAlive: ",th.is_alive())
        joy_threads.append(t)
        t.start()

def close_window():
    sys.exit()
    print( "Window closed")

def msg_ok_click():
   print('OK button clicked!')

root = tk.Tk()
app = App(root)

if __name__ == "__main__":

    t = Thread(target=keyboardListenThread, args=(app,))
    t.start()
    threads.append(t)
    
    t2 = Thread(target=mouseListenThread, args=(app,))
    t2.start()
    threads.append(t2)

    Thread(target=searchJoystick).start()

    root.protocol("WM_DELETE_WINDOW", close_window)
    root.mainloop()
