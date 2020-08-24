#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import threading  # 线程 一直接收数据，不影响主线程运行
import tkinter
from tkinter import *
from tkinter import ttk
# from tkinter import Tk, Label, Text, Button, END
import time
from SerialClass import SerialAchieve  # 导入串口通讯类

LOG_LINE_NUM = 0
LOG_RT_NUM = 0
w1 = 8  # 上面5*10个方格的宽
h1 = 2  # 上面5*10个方格的高
x1 = [0.05 + 0.1 * i for i in range(10)]
y1 = [0.1 + 0.1 * i for i in range(5)]

w2 = 6  # 下面5*10个方格的宽
h2 = 1  # 下面5*10个方格的高
x2 = [0.05 + 0.07 * i for i in range(13)]
y2 = [0.6 + 0.05 * i for i in range(5)]

port_ls = 1  # 默认有端口
port_opened = 0  # 串口连接标志，默认未连接
button_pressed = 0  # 接收按钮按下标志，默认未按下


class MY_GUI(object):
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        # 定义串口变量 08.19
        self.port = None
        self.band = None
        self.check = None
        self.data = None
        self.stop = None
        self.myserial = None

    # 设置窗口  mainwin = init_window_name
    def set_init_window(self):
        self.init_window_name.title("温度显示工具_v2.0")  # 窗口名
        self.init_window_name.geometry('1068x681+10+10')  # 290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name["bg"] = "#FFF8DC"  # 窗口背景色，其他背景色见：https://www.bejson.com/convert/rgbhex/
        self.init_window_name.attributes("-alpha", 1)  # 虚化，值越小虚化程度越高
        # self.init_window_name.iconbitmap('wen.ico')  # 会引起错误，路径找不到
        # self.init_window_name.resizable(0, 0)   # 固定屏幕尺寸

        """
        自己的显示框  5*10 y=0.1-0.5
        """
        global w1, w2, h1, h2
        global x1, x2, y1, y2
        global port_ls
        self.in_data_label = Label(self.init_window_name, text="温度显示", bg="#F8F8FF")  # 输入标签 init_data_label
        self.in_data_label.place(relx=0.05, rely=0.02, anchor=CENTER)
        # self.result_data_label = Label(self.init_window_name, text="输出结果")  # 输出标签 result_data_label
        # self.result_data_label.place(relx=0.6, rely=0.02, anchor=CENTER)

        # for i in range(5):   # 可以生成方框，但是无法赋值。
        #     for j in range(10):
        #         b='self.in_data_'+str(i*10+j).zfill(2)
        #         print(b)
        #
        #         b=Text(self.init_window_name, width=w1, height=h1)
        #         b.place(relx=0.05+0.1*j, rely=0.1*(i+1), anchor=CENTER)

        self.in_data_00 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_00.place(relx=x1[0], rely=y1[0], anchor=CENTER)
        self.in_data_01 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_01.place(relx=x1[1], rely=y1[0], anchor=CENTER)
        self.in_data_02 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_02.place(relx=x1[2], rely=y1[0], anchor=CENTER)
        self.in_data_03 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_03.place(relx=x1[3], rely=y1[0], anchor=CENTER)
        self.in_data_04 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_04.place(relx=x1[4], rely=y1[0], anchor=CENTER)
        self.in_data_05 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_05.place(relx=x1[5], rely=y1[0], anchor=CENTER)
        self.in_data_06 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_06.place(relx=x1[6], rely=y1[0], anchor=CENTER)
        self.in_data_07 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_07.place(relx=x1[7], rely=y1[0], anchor=CENTER)
        self.in_data_08 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_08.place(relx=x1[8], rely=y1[0], anchor=CENTER)
        self.in_data_09 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_09.place(relx=x1[9], rely=y1[0], anchor=CENTER)

        self.in_data_10 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_10.place(relx=x1[0], rely=y1[1], anchor=CENTER)
        self.in_data_11 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_11.place(relx=x1[1], rely=y1[1], anchor=CENTER)
        self.in_data_12 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_12.place(relx=x1[2], rely=y1[1], anchor=CENTER)
        self.in_data_13 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_13.place(relx=x1[3], rely=y1[1], anchor=CENTER)
        self.in_data_14 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_14.place(relx=x1[4], rely=y1[1], anchor=CENTER)
        self.in_data_15 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_15.place(relx=x1[5], rely=y1[1], anchor=CENTER)
        self.in_data_16 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_16.place(relx=x1[6], rely=y1[1], anchor=CENTER)
        self.in_data_17 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_17.place(relx=x1[7], rely=y1[1], anchor=CENTER)
        self.in_data_18 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_18.place(relx=x1[8], rely=y1[1], anchor=CENTER)
        self.in_data_19 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_19.place(relx=x1[9], rely=y1[1], anchor=CENTER)

        self.in_data_20 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_20.place(relx=x1[0], rely=y1[2], anchor=CENTER)
        self.in_data_21 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_21.place(relx=x1[1], rely=y1[2], anchor=CENTER)
        self.in_data_22 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_22.place(relx=x1[2], rely=y1[2], anchor=CENTER)
        self.in_data_23 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_23.place(relx=x1[3], rely=y1[2], anchor=CENTER)
        self.in_data_24 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_24.place(relx=x1[4], rely=y1[2], anchor=CENTER)
        self.in_data_25 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_25.place(relx=x1[5], rely=y1[2], anchor=CENTER)
        self.in_data_26 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_26.place(relx=x1[6], rely=y1[2], anchor=CENTER)
        self.in_data_27 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_27.place(relx=x1[7], rely=y1[2], anchor=CENTER)
        self.in_data_28 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_28.place(relx=x1[8], rely=y1[2], anchor=CENTER)
        self.in_data_29 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_29.place(relx=x1[9], rely=y1[2], anchor=CENTER)

        self.in_data_30 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_30.place(relx=x1[0], rely=y1[3], anchor=CENTER)
        self.in_data_31 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_31.place(relx=x1[1], rely=y1[3], anchor=CENTER)
        self.in_data_32 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_32.place(relx=x1[2], rely=y1[3], anchor=CENTER)
        self.in_data_33 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_33.place(relx=x1[3], rely=y1[3], anchor=CENTER)
        self.in_data_34 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_34.place(relx=x1[4], rely=y1[3], anchor=CENTER)
        self.in_data_35 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_35.place(relx=x1[5], rely=y1[3], anchor=CENTER)
        self.in_data_36 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_36.place(relx=x1[6], rely=y1[3], anchor=CENTER)
        self.in_data_37 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_37.place(relx=x1[7], rely=y1[3], anchor=CENTER)
        self.in_data_38 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_38.place(relx=x1[8], rely=y1[3], anchor=CENTER)
        self.in_data_39 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_39.place(relx=x1[9], rely=y1[3], anchor=CENTER)

        self.in_data_40 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_40.place(relx=x1[0], rely=y1[4], anchor=CENTER)
        self.in_data_41 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_41.place(relx=x1[1], rely=y1[4], anchor=CENTER)
        self.in_data_42 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_42.place(relx=x1[2], rely=y1[4], anchor=CENTER)
        self.in_data_43 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_43.place(relx=x1[3], rely=y1[4], anchor=CENTER)
        self.in_data_44 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_44.place(relx=x1[4], rely=y1[4], anchor=CENTER)
        self.in_data_45 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_45.place(relx=x1[5], rely=y1[4], anchor=CENTER)
        self.in_data_46 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_46.place(relx=x1[6], rely=y1[4], anchor=CENTER)
        self.in_data_47 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_47.place(relx=x1[7], rely=y1[4], anchor=CENTER)
        self.in_data_48 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_48.place(relx=x1[8], rely=y1[4], anchor=CENTER)
        self.in_data_49 = Text(self.init_window_name, width=w1, height=h1)  # 原始数据录入框 init_data_Text
        self.in_data_49.place(relx=x1[9], rely=y1[4], anchor=CENTER)

        """
        中间横线  y=0.5-0.6
        """
        self.w = Canvas(self.init_window_name, width=2000, height=10)  # 实际线宽由 height=10控制
        self.w.create_line(0, 0, 2000, 0, fill="red", width=30, capstyle=ROUND)  # 真实线宽 多余的被Canvas()遮挡了
        self.w.place(relx=0.5, rely=0.56, anchor=CENTER)  # Canvas上中心点位置

        """
        下端5*10个框 y=0.6-1.0
        """
        self.out_data_00 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_00.place(relx=x2[0], rely=y2[0], anchor=CENTER)
        self.out_data_01 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_01.place(relx=x2[1], rely=y2[0], anchor=CENTER)
        self.out_data_02 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_02.place(relx=x2[2], rely=y2[0], anchor=CENTER)
        self.out_data_03 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_03.place(relx=x2[3], rely=y2[0], anchor=CENTER)
        self.out_data_04 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_04.place(relx=x2[4], rely=y2[0], anchor=CENTER)
        self.out_data_05 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_05.place(relx=x2[5], rely=y2[0], anchor=CENTER)
        self.out_data_06 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_06.place(relx=x2[6], rely=y2[0], anchor=CENTER)
        self.out_data_07 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_07.place(relx=x2[7], rely=y2[0], anchor=CENTER)
        self.out_data_08 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_08.place(relx=x2[8], rely=y2[0], anchor=CENTER)
        self.out_data_09 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_09.place(relx=x2[9], rely=y2[0], anchor=CENTER)

        self.out_data_10 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_10.place(relx=x2[0], rely=y2[1], anchor=CENTER)
        self.out_data_11 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_11.place(relx=x2[1], rely=y2[1], anchor=CENTER)
        self.out_data_12 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_12.place(relx=x2[2], rely=y2[1], anchor=CENTER)
        self.out_data_13 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_13.place(relx=x2[3], rely=y2[1], anchor=CENTER)
        self.out_data_14 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_14.place(relx=x2[4], rely=y2[1], anchor=CENTER)
        self.out_data_15 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_15.place(relx=x2[5], rely=y2[1], anchor=CENTER)
        self.out_data_16 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_16.place(relx=x2[6], rely=y2[1], anchor=CENTER)
        self.out_data_17 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_17.place(relx=x2[7], rely=y2[1], anchor=CENTER)
        self.out_data_18 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_18.place(relx=x2[8], rely=y2[1], anchor=CENTER)
        self.out_data_19 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_19.place(relx=x2[9], rely=y2[1], anchor=CENTER)

        self.out_data_20 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_20.place(relx=x2[0], rely=y2[2], anchor=CENTER)
        self.out_data_21 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_21.place(relx=x2[1], rely=y2[2], anchor=CENTER)
        self.out_data_22 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_22.place(relx=x2[2], rely=y2[2], anchor=CENTER)
        self.out_data_23 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_23.place(relx=x2[3], rely=y2[2], anchor=CENTER)
        self.out_data_24 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_24.place(relx=x2[4], rely=y2[2], anchor=CENTER)
        self.out_data_25 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_25.place(relx=x2[5], rely=y2[2], anchor=CENTER)
        self.out_data_26 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_26.place(relx=x2[6], rely=y2[2], anchor=CENTER)
        self.out_data_27 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_27.place(relx=x2[7], rely=y2[2], anchor=CENTER)
        self.out_data_28 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_28.place(relx=x2[8], rely=y2[2], anchor=CENTER)
        self.out_data_29 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_29.place(relx=x2[9], rely=y2[2], anchor=CENTER)

        self.out_data_30 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_30.place(relx=x2[0], rely=y2[3], anchor=CENTER)
        self.out_data_31 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_31.place(relx=x2[1], rely=y2[3], anchor=CENTER)
        self.out_data_32 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_32.place(relx=x2[2], rely=y2[3], anchor=CENTER)
        self.out_data_33 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_33.place(relx=x2[3], rely=y2[3], anchor=CENTER)
        self.out_data_34 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_34.place(relx=x2[4], rely=y2[3], anchor=CENTER)
        self.out_data_35 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_35.place(relx=x2[5], rely=y2[3], anchor=CENTER)
        self.out_data_36 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_36.place(relx=x2[6], rely=y2[3], anchor=CENTER)
        self.out_data_37 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_37.place(relx=x2[7], rely=y2[3], anchor=CENTER)
        self.out_data_38 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_38.place(relx=x2[8], rely=y2[3], anchor=CENTER)
        self.out_data_39 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_39.place(relx=x2[9], rely=y2[3], anchor=CENTER)

        self.out_data_40 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_40.place(relx=x2[0], rely=y2[4], anchor=CENTER)
        self.out_data_41 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_41.place(relx=x2[1], rely=y2[4], anchor=CENTER)
        self.out_data_42 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_42.place(relx=x2[2], rely=y2[4], anchor=CENTER)
        self.out_data_43 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_43.place(relx=x2[3], rely=y2[4], anchor=CENTER)
        self.out_data_44 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_44.place(relx=x2[4], rely=y2[4], anchor=CENTER)
        self.out_data_45 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_45.place(relx=x2[5], rely=y2[4], anchor=CENTER)
        self.out_data_46 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_46.place(relx=x2[6], rely=y2[4], anchor=CENTER)
        self.out_data_47 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_47.place(relx=x2[7], rely=y2[4], anchor=CENTER)
        self.out_data_48 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_48.place(relx=x2[8], rely=y2[4], anchor=CENTER)
        self.out_data_49 = Text(self.init_window_name, width=w2, height=h2)  # 原始数据录入框 init_data_Text
        self.out_data_49.place(relx=x2[9], rely=y2[4], anchor=CENTER)

        """
        温度设置按钮 bg="green"
        """
        self.wendu_button = Button(self.init_window_name, text="温度设置",
                                   command=self.wendu_trans, font=("宋体", 10), width=10,
                                   height=h2, bg="#8470FF")  # 按钮 调用内部方法  加()为直接调用
        self.wendu_button.place(relx=x2[2], rely=0.85, anchor=CENTER)

        # 温度设置标签
        self.out_data_label = Label(self.init_window_name, text="温度设置", bg="#F8F8FF")  # 输入标签 init_data_label
        self.out_data_label.place(relx=0.05, rely=0.56, anchor=CENTER)
        self.wendu_label = Label(self.init_window_name, text="温度设置结果", bg="#F8F8FF")  # 日志标签 log_label
        self.wendu_label.place(relx=0.056, rely=0.85, anchor=CENTER)

        # 串口标签 08.19
        self.label1 = Label(self.init_window_name, text="串口号:", font=("宋体", 10), bg="#F8F8FF")
        self.label1.place(relx=0.02 + x2[10], rely=y2[0], anchor=CENTER)
        self.label2 = Label(self.init_window_name, text="波特率:", font=("宋体", 10), bg="#F8F8FF")
        self.label2.place(relx=0.02 + x2[10], rely=y2[1], anchor=CENTER)
        # self.label3 = Label(self.init_window_name, text="校验位:", font=("宋体", 10))  # 无作用 去掉腾空间
        # self.label3.place(relx=0.02+x2[10], rely=y2[2], anchor=CENTER)
        # self.label4 = Label(self.init_window_name, text="数据位:", font=("宋体", 10))
        # self.label4.place(relx=0.02+x2[10], rely=y2[3], anchor=CENTER)
        # self.label5 = Label(self.init_window_name, text="停止位:", font=("宋体", 10))
        # self.label5.place(relx=0.02+x2[10], rely=y2[4], anchor=CENTER)

        # 串口文本显示，清除发送数据 08.19
        self.label6 = Label(self.init_window_name, text="已发送数据:", font=("宋体", 10), bg="#F8F8FF")
        self.label6.place(relx=0.34, rely=0.85, anchor=CENTER)
        self.label7 = Label(self.init_window_name, text="已接收数据:", font=("宋体", 10), bg="#F8F8FF")
        self.label7.place(relx=0.55, rely=0.85, anchor=CENTER)

        # 串口传输显示 08.20
        self.label8 = Label(self.init_window_name, text="串口日志：", font=("宋体", 10), bg="#F8F8FF")
        self.label8.place(relx=0.78, rely=0.85, anchor=CENTER)

        # 串口输入 08.21
        self.label9 = Label(self.init_window_name, text="待发送数据：", font=("宋体", 10), bg="#F8F8FF")
        self.label9.place(relx=0.78, rely=y2[3], anchor=CENTER)

        # 串口号 08.19
        self.com1value = StringVar()  # 窗体中自带的文本，创建一个值
        self.combobox_port = ttk.Combobox(self.init_window_name, textvariable=self.com1value,
                                          width=w2, font=("宋体", 10))
        # 输入选定内容 08.19
        self.combobox_port["value"] = [""]  # 这里先选定
        self.combobox_port.place(relx=0.03 + x2[11], rely=y2[0], anchor=CENTER)  # 显示

        # 波特率 08.19
        self.bandvalue = StringVar()  # 窗体中自带的文本，创建一个值
        self.combobox_band = ttk.Combobox(self.init_window_name, textvariable=self.bandvalue, width=w2, font=("宋体", 10))
        # 输入选定内容 08.19
        self.combobox_band["value"] = ["4800", "9600", "14400", "19200", "38400", "57600", "115200"]  # 这里先选定
        self.combobox_band.current(1)  # 默认选中第0个
        self.combobox_band.place(relx=0.03 + x2[11], rely=y2[1], anchor=CENTER)  # 显示

        # 校验位 08.19
        # self.checkvalue = StringVar()  # 窗体中自带的文本，创建一个值
        self.checkvalue = 'w'  # 窗体中自带的文本，创建一个值

        # self.combobox_check = ttk.Combobox(self.init_window_name, textvariable=self.checkvalue, width=w2,
        #                                    font=("宋体", 10))
        # 输入选定内容 08.19
        # self.combobox_check["value"] = ["无校验"]  # 这里先选定
        # self.combobox_check.current(0)  # 默认选中第0个
        # self.combobox_check.place(relx=0.03+x2[11], rely=y2[2], anchor=CENTER)  # 显示

        # # 数据位 08.19
        # self.datavalue = StringVar()  # 窗体中自带的文本，创建一个值
        # self.combobox_data = ttk.Combobox(self.init_window_name, textvariable=self.datavalue, width=w2, font=("宋体", 10))
        # # 输入选定内容 08.19
        # self.combobox_data["value"] = ["8", "9", "0"]  # 这里先选定
        # self.combobox_data.current(0)  # 默认选中第0个
        # self.combobox_data.place(relx=0.03+x2[11], rely=y2[3], anchor=CENTER)  # 显示
        #
        # # 停止位 08.19
        # self.stopvalue = StringVar()  # 窗体中自带的文本，创建一个值
        # self.combobox_stop = ttk.Combobox(self.init_window_name, textvariable=self.stopvalue, width=w2, font=("宋体", 10))
        # # 输入选定内容 08.19
        # self.combobox_stop["value"] = ["1", "0"]  # 这里先选定
        # self.combobox_stop.current(0)  # 默认选中第0个
        # self.combobox_stop.place(relx=0.03+x2[11], rely=y2[4], anchor=CENTER)  # 显示

        # 获取界面的参数 08.19
        self.band = self.combobox_band.get()
        # self.check = self.combobox_check.get()
        self.check = 'no'
        # self.data = self.combobox_data.get()
        self.data = 'no'
        # self.stop = self.combobox_stop.get()
        self.stop = 'no'
        print("波特率：" + self.band)
        self.myserial = SerialAchieve(int(self.band), self.check, self.data, self.stop)

        # 处理串口值 08.19  需要在’打开串口‘之前运行以刷新port_ls的值
        self.port_list = self.myserial.get_port()
        port_str_list = []  # 用来存储切割好的串口号
        for i in range(len(self.port_list)):
            lines = str(self.port_list[i])
            str_list = lines.split(" ")
            port_str_list.append(str_list[0])
        self.combobox_port["value"] = port_str_list
        if port_str_list:
            self.combobox_port.current(0)  # 默认选中第0个
            port_ls = 1
        else:
            self.combobox_port.current()  # 默认不选
            port_ls = 0

        # 按键显示，打开串口 08.19
        if port_ls == 1:
            self.button_OK = Button(self.init_window_name, text="打开串口",
                                    command=self.button_OK_click_1, font=("宋体", 10),
                                    width=9, height=h2, bg="#FF8C00")
        else:
            self.button_OK = Button(self.init_window_name, text="打开串口",
                                    command=self.button_OK_click_0, font=("宋体", 10),
                                    width=9, height=h2, bg="#FF8C00")
        self.button_OK.place(relx=0.05 + x2[12], rely=y2[0], anchor=CENTER)  # 显示控件
        # 关闭串口 08.19
        self.button_Cancel = Button(self.init_window_name, text="关闭串口",  # 显示文本
                                    command=self.button_Cancel_click, font=("宋体", 10),
                                    width=9, height=h2, bg="#FF8C00")
        self.button_Cancel.place(relx=0.05 + x2[12], rely=y2[1], anchor=CENTER)  # 显示控件

        # 发送按键 08.19
        self.button_Send = Button(self.init_window_name, text="发送",  # 显示文本
                                  command=self.button_Send_click, font=("宋体", 10),
                                  width=9, height=h2, bg="#ADFF2F")
        self.button_Send.place(relx=0.03 + x2[11], rely=y2[2], anchor=CENTER)  # 显示控件
        # 接收按键 08.19
        self.button_Rece = Button(self.init_window_name, text="接收",  # 显示文本
                                  command=self.button_Rece_click, font=("宋体", 10),
                                  width=9, height=h2, bg="#ADFF2F")
        self.button_Rece.place(relx=0.05 + x2[12], rely=y2[2], anchor=CENTER)  # 显示控件

        # 清除发送数据 08.19
        self.button_Cancel = Button(self.init_window_name, text="清除已发送数据",  # 显示文本
                                    command=self.button_clcSend_click, font=("宋体", 10),
                                    width=13, height=h2, bg="#F0FFFF")
        self.button_Cancel.place(relx=0.445, rely=0.85, anchor=CENTER)  # 显示控件
        # 清除接收数据 08.19
        self.button_Cancel = Button(self.init_window_name, text="清除已接收数据",  # 显示文本
                                    command=self.button_clcRece_click, font=("宋体", 10),
                                    width=13, height=h2, bg="#F0FFFF")
        self.button_Cancel.place(relx=0.654, rely=0.85, anchor=CENTER)  # 显示控件

        # 温度设置

        self.wendu_data = Text(self.init_window_name, width=38, height=5)  # 日志结果
        self.wendu_data.place(relx=0.155, rely=0.93, anchor=CENTER)

        # 显示框 08.19
        # 实现记事本的功能组件
        self.SendDataView = Text(self.init_window_name, width=28, height=5,
                                 font=("宋体", 10))  # text实际上是一个文本编辑器
        self.SendDataView.place(relx=0.40, rely=0.93, anchor=CENTER)  # 显示
        self.ReceDataView = Text(self.init_window_name, width=28, height=5,
                                 font=("宋体", 10))  # text实际上是一个文本编辑器
        self.ReceDataView.place(relx=0.61, rely=0.93, anchor=CENTER)  # 显示
        # 显示串口日志 08.20
        self.RT_Data = Text(self.init_window_name, width=33, height=5,
                            font=("宋体", 10))  # text实际上是一个文本编辑器
        self.RT_Data.place(relx=0.86, rely=0.93, anchor=CENTER)  # 显示

        # 发送的内容 08.19
        test_str = StringVar(value="Hello")
        self.entrySend = Entry(self.init_window_name, width=33, textvariable=test_str, font=("宋体", 10))
        self.entrySend.place(relx=0.86, rely=y2[4], anchor=CENTER)  # 显示

    # 温度按钮 功能函数
    def wendu_trans(self):
        src_00 = self.out_data_00.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_00:
            try:  # 运行正确
                wendu_num = round(float(src_00), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_00.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_00.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_00.delete(1.0, END)
                self.in_data_00.insert(1.0, "温度写入失败00")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_01 = self.out_data_01.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_01:
            try:  # 运行正确
                wendu_num = round(float(src_01), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_01.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_01.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_01.delete(1.0, END)
                self.in_data_01.insert(1.0, "温度写入失败01")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_02 = self.out_data_02.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_02:
            try:  # 运行正确
                wendu_num = round(float(src_02), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_02.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_02.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_02.delete(1.0, END)
                self.in_data_02.insert(1.0, "温度写入失败02")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_03 = self.out_data_03.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_03:
            try:  # 运行正确
                wendu_num = round(float(src_03), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_03.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_03.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_03.delete(1.0, END)
                self.in_data_03.insert(1.0, "温度写入失败03")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_04 = self.out_data_04.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_04:
            try:  # 运行正确
                wendu_num = round(float(src_04), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_04.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_04.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_04.delete(1.0, END)
                self.in_data_04.insert(1.0, "温度写入失败04")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_05 = self.out_data_05.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_05:
            try:  # 运行正确
                wendu_num = round(float(src_05), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_05.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_05.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_05.delete(1.0, END)
                self.in_data_05.insert(1.0, "温度写入失败05")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_06 = self.out_data_06.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_06:
            try:  # 运行正确
                wendu_num = round(float(src_06), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_06.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_06.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_06.delete(1.0, END)
                self.in_data_06.insert(1.0, "温度写入失败06")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_07 = self.out_data_07.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_07:
            try:  # 运行正确
                wendu_num = round(float(src_07), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_07.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_07.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_07.delete(1.0, END)
                self.in_data_07.insert(1.0, "温度写入失败07")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_08 = self.out_data_08.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_08:
            try:  # 运行正确
                wendu_num = round(float(src_08), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_08.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_08.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_08.delete(1.0, END)
                self.in_data_08.insert(1.0, "温度写入失败08")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_09 = self.out_data_09.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_09:
            try:  # 运行正确
                wendu_num = round(float(src_09), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_09.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_09.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_09.delete(1.0, END)
                self.in_data_09.insert(1.0, "温度写入失败09")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_10 = self.out_data_10.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_10:
            try:  # 运行正确
                wendu_num = round(float(src_10), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_10.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_10.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_10.delete(1.0, END)
                self.in_data_10.insert(1.0, "温度写入失败10")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_11 = self.out_data_11.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_11:
            try:  # 运行正确
                wendu_num = round(float(src_11), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_11.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_11.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_11.delete(1.0, END)
                self.in_data_11.insert(1.0, "温度写入失败11")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_12 = self.out_data_12.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_12:
            try:  # 运行正确
                wendu_num = round(float(src_12), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_12.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_12.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_12.delete(1.0, END)
                self.in_data_12.insert(1.0, "温度写入失败12")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_13 = self.out_data_13.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_13:
            try:  # 运行正确
                wendu_num = round(float(src_13), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_13.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_13.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_13.delete(1.0, END)
                self.in_data_13.insert(1.0, "温度写入失败13")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_14 = self.out_data_14.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_14:
            try:  # 运行正确
                wendu_num = round(float(src_14), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_14.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_14.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_14.delete(1.0, END)
                self.in_data_14.insert(1.0, "温度写入失败14")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_15 = self.out_data_15.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_15:
            try:  # 运行正确
                wendu_num = round(float(src_15), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_15.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_15.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_15.delete(1.0, END)
                self.in_data_15.insert(1.0, "温度写入失败15")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_16 = self.out_data_16.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_16:
            try:  # 运行正确
                wendu_num = round(float(src_16), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_16.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_16.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_16.delete(1.0, END)
                self.in_data_16.insert(1.0, "温度写入失败16")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_17 = self.out_data_17.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_17:
            try:  # 运行正确
                wendu_num = round(float(src_17), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_17.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_17.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_17.delete(1.0, END)
                self.in_data_17.insert(1.0, "温度写入失败17")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_18 = self.out_data_18.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_18:
            try:  # 运行正确
                wendu_num = round(float(src_18), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_18.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_18.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_18.delete(1.0, END)
                self.in_data_18.insert(1.0, "温度写入失败18")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_19 = self.out_data_19.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_19:
            try:  # 运行正确
                wendu_num = round(float(src_19), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_19.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_19.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_19.delete(1.0, END)
                self.in_data_19.insert(1.0, "温度写入失败19")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_20 = self.out_data_20.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_20:
            try:  # 运行正确
                wendu_num = round(float(src_20), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_20.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_20.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_20.delete(1.0, END)
                self.in_data_20.insert(1.0, "温度写入失败20")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_21 = self.out_data_21.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_21:
            try:  # 运行正确
                wendu_num = round(float(src_21), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_21.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_21.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_21.delete(1.0, END)
                self.in_data_21.insert(1.0, "温度写入失败21")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_22 = self.out_data_22.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_22:
            try:  # 运行正确
                wendu_num = round(float(src_22), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_22.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_22.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_22.delete(1.0, END)
                self.in_data_22.insert(1.0, "温度写入失败22")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_23 = self.out_data_23.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_23:
            try:  # 运行正确
                wendu_num = round(float(src_23), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_23.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_23.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_23.delete(1.0, END)
                self.in_data_23.insert(1.0, "温度写入失败23")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_24 = self.out_data_24.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_24:
            try:  # 运行正确
                wendu_num = round(float(src_24), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_24.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_24.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_24.delete(1.0, END)
                self.in_data_24.insert(1.0, "温度写入失败24")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_25 = self.out_data_25.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_25:
            try:  # 运行正确
                wendu_num = round(float(src_25), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_25.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_25.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_25.delete(1.0, END)
                self.in_data_25.insert(1.0, "温度写入失败25")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_26 = self.out_data_26.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_26:
            try:  # 运行正确
                wendu_num = round(float(src_26), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_26.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_26.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_26.delete(1.0, END)
                self.in_data_26.insert(1.0, "温度写入失败26")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_27 = self.out_data_27.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_27:
            try:  # 运行正确
                wendu_num = round(float(src_27), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_27.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_27.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_27.delete(1.0, END)
                self.in_data_27.insert(1.0, "温度写入失败27")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_28 = self.out_data_28.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_28:
            try:  # 运行正确
                wendu_num = round(float(src_28), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_28.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_28.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_28.delete(1.0, END)
                self.in_data_28.insert(1.0, "温度写入失败28")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_29 = self.out_data_29.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_29:
            try:  # 运行正确
                wendu_num = round(float(src_29), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_29.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_29.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_29.delete(1.0, END)
                self.in_data_29.insert(1.0, "温度写入失败29")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_30 = self.out_data_30.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_30:
            try:  # 运行正确
                wendu_num = round(float(src_30), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_30.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_30.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_30.delete(1.0, END)
                self.in_data_30.insert(1.0, "温度写入失败30")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_31 = self.out_data_31.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_31:
            try:  # 运行正确
                wendu_num = round(float(src_31), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_31.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_31.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_31.delete(1.0, END)
                self.in_data_31.insert(1.0, "温度写入失败31")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_32 = self.out_data_32.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_32:
            try:  # 运行正确
                wendu_num = round(float(src_32), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_32.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_32.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_32.delete(1.0, END)
                self.in_data_32.insert(1.0, "温度写入失败32")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_33 = self.out_data_33.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_33:
            try:  # 运行正确
                wendu_num = round(float(src_33), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_33.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_33.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_33.delete(1.0, END)
                self.in_data_33.insert(1.0, "温度写入失败33")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_34 = self.out_data_34.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_34:
            try:  # 运行正确
                wendu_num = round(float(src_34), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_34.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_34.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_34.delete(1.0, END)
                self.in_data_34.insert(1.0, "温度写入失败34")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_35 = self.out_data_35.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_35:
            try:  # 运行正确
                wendu_num = round(float(src_35), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_35.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_35.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_35.delete(1.0, END)
                self.in_data_35.insert(1.0, "温度写入失败35")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_36 = self.out_data_36.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_36:
            try:  # 运行正确
                wendu_num = round(float(src_36), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_36.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_36.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_36.delete(1.0, END)
                self.in_data_36.insert(1.0, "温度写入失败36")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_37 = self.out_data_37.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_37:
            try:  # 运行正确
                wendu_num = round(float(src_37), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_37.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_37.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_37.delete(1.0, END)
                self.in_data_37.insert(1.0, "温度写入失败37")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_38 = self.out_data_38.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_38:
            try:  # 运行正确
                wendu_num = round(float(src_38), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_38.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_38.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_38.delete(1.0, END)
                self.in_data_38.insert(1.0, "温度写入失败38")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_39 = self.out_data_39.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_39:
            try:  # 运行正确
                wendu_num = round(float(src_39), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_39.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_39.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_39.delete(1.0, END)
                self.in_data_39.insert(1.0, "温度写入失败39")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_40 = self.out_data_40.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_40:
            try:  # 运行正确
                wendu_num = round(float(src_40), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_40.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_40.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_40.delete(1.0, END)
                self.in_data_40.insert(1.0, "温度写入失败40")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_41 = self.out_data_41.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_41:
            try:  # 运行正确
                wendu_num = round(float(src_41), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_41.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_41.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_41.delete(1.0, END)
                self.in_data_41.insert(1.0, "温度写入失败41")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_42 = self.out_data_42.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_42:
            try:  # 运行正确
                wendu_num = round(float(src_42), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_42.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_42.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_42.delete(1.0, END)
                self.in_data_42.insert(1.0, "温度写入失败42")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_43 = self.out_data_43.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_43:
            try:  # 运行正确
                wendu_num = round(float(src_43), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_43.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_43.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_43.delete(1.0, END)
                self.in_data_43.insert(1.0, "温度写入失败43")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_44 = self.out_data_44.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_44:
            try:  # 运行正确
                wendu_num = round(float(src_44), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_44.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_44.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_44.delete(1.0, END)
                self.in_data_44.insert(1.0, "温度写入失败44")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_45 = self.out_data_45.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_45:
            try:  # 运行正确
                wendu_num = round(float(src_45), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_45.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_45.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_45.delete(1.0, END)
                self.in_data_45.insert(1.0, "温度写入失败45")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_46 = self.out_data_46.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_46:
            try:  # 运行正确
                wendu_num = round(float(src_46), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_46.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_46.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_46.delete(1.0, END)
                self.in_data_46.insert(1.0, "温度写入失败46")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_47 = self.out_data_47.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_47:
            try:  # 运行正确
                wendu_num = round(float(src_47), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_47.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_47.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_47.delete(1.0, END)
                self.in_data_47.insert(1.0, "温度写入失败47")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_48 = self.out_data_48.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_48:
            try:  # 运行正确
                wendu_num = round(float(src_48), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_48.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_48.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_48.delete(1.0, END)
                self.in_data_48.insert(1.0, "温度写入失败48")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_49 = self.out_data_49.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        if src_49:
            try:  # 运行正确
                wendu_num = round(float(src_49), 1)  # 保留一位小数
                print(wendu_num)
                self.in_data_49.delete(1.0, END)  # 删除（delete）界面中原来的值
                self.in_data_49.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_49.delete(1.0, END)
                self.in_data_49.insert(1.0, "温度写入失败49")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

    # 获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    # 日志动态打印
    def write_wendu_log(self, logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        if LOG_LINE_NUM <= 3:
            self.wendu_data.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.wendu_data.delete(1.0, 2.0)  # 将之前的第1、2个数据删掉
            self.wendu_data.insert(END, logmsg_in)

    """串口部分 2020.08.19 https://www.cnblogs.com/zhicungaoyuan-mingzhi/p/12303229.html"""
    def button_Cancel_click(self):  # 关闭串口 按钮
        global port_opened, button_pressed
        port_opened = 0  # 串口状态为0
        button_pressed = 0  # 接收按钮状态为0
        self.myserial.delete_port()
        self.write_rt_log("关闭串口成功")  # 调用写入日志函数
        print("关闭串口成功")

    def Receive_Data(self):  # 一直接收函数 08.20
        global button_pressed
        if button_pressed == 0:
            if port_ls == 1:  # 如果有串口（不一定连接了）
                while self.myserial.port.isOpen():
                    readstr = self.myserial.Read_data()
                    print(readstr, type(readstr))
                    # 数据分割
                    c = re.compile(r'(\s*[\d]+[.]?[\d]{0,5}\s*)')  # 至少1个数字 + 0或者1个小数点 + 任意个数字 (前后可以有空格)
                    c1 = re.compile(r'a(\s*[\d]+[.]?[\d]{0,5}\s*)b')  # 校验第5个测量的温度 数据格式a23.23b，其中a和b之间的23.23为第五个温度数据
                    c2 = re.compile(r'c(\s*[\d]+[.]?[\d]{0,5}\s*)d')  # 校验第5个测量的温度 数据格式c23.23d，其中a和b之间的23.23为第十个温度数据
                    cc = c.findall(readstr)
                    cc1 = c1.findall(readstr)
                    cc2 = c2.findall(readstr)
                    print(cc, cc1, cc2)
                    try:
                        if int(cc1[0]) == int(cc[4]) and int(cc2[0]) == int(cc[9]):  # 数据校验，是否丢失和错位
                            print('cc right')  # 数据正确，将每个数据放在对应的框里

                            self.in_data_00.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_00.insert(1.0, str(int(cc[0])) + '°C')  # 插入（insert）新的md5值
                            self.in_data_01.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_01.insert(1.0, str(int(cc[1])) + '°C')  # 插入（insert）新的md5值
                            self.in_data_02.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_02.insert(1.0, str(int(cc[2])) + '°C')  # 插入（insert）新的md5值
                            self.in_data_03.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_03.insert(1.0, str(int(cc[3])) + '°C')  # 插入（insert）新的md5值
                            self.in_data_04.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_04.insert(1.0, str(int(cc[4])) + '°C')  # 插入（insert）新的md5值
                            self.in_data_05.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_05.insert(1.0, str(int(cc[5])) + '°C')  # 插入（insert）新的md5值
                            self.in_data_06.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_06.insert(1.0, str(int(cc[6])) + '°C')  # 插入（insert）新的md5值
                            self.in_data_07.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_07.insert(1.0, str(int(cc[7])) + '°C')  # 插入（insert）新的md5值
                            self.in_data_08.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_08.insert(1.0, str(int(cc[8])) + '°C')  # 插入（insert）新的md5值
                            self.in_data_09.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_09.insert(1.0, str(int(cc[9])) + '°C')  # 插入（insert）新的md5值

                            self.in_data_10.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_10.insert(1.0, int(cc[10]))  # 插入（insert）新的md5值
                            self.in_data_11.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_11.insert(1.0, int(cc[11]))  # 插入（insert）新的md5值
                            self.in_data_12.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_12.insert(1.0, int(cc[12]))  # 插入（insert）新的md5值
                            self.in_data_13.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_13.insert(1.0, int(cc[13]))  # 插入（insert）新的md5值
                            self.in_data_14.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_14.insert(1.0, int(cc[14]))  # 插入（insert）新的md5值
                            self.in_data_15.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_15.insert(1.0, int(cc[15]))  # 插入（insert）新的md5值
                            self.in_data_16.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_16.insert(1.0, int(cc[16]))  # 插入（insert）新的md5值
                            self.in_data_17.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_17.insert(1.0, int(cc[17]))  # 插入（insert）新的md5值
                            self.in_data_18.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_18.insert(1.0, int(cc[18]))  # 插入（insert）新的md5值
                            self.in_data_19.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_19.insert(1.0, int(cc[19]))  # 插入（insert）新的md5值

                            self.in_data_20.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_20.insert(1.0, int(cc[20]))  # 插入（insert）新的md5值
                            self.in_data_21.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_21.insert(1.0, int(cc[21]))  # 插入（insert）新的md5值
                            self.in_data_22.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_22.insert(1.0, int(cc[22]))  # 插入（insert）新的md5值
                            self.in_data_23.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_23.insert(1.0, int(cc[23]))  # 插入（insert）新的md5值
                            self.in_data_24.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_24.insert(1.0, int(cc[24]))  # 插入（insert）新的md5值
                            self.in_data_25.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_25.insert(1.0, int(cc[25]))  # 插入（insert）新的md5值
                            self.in_data_26.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_26.insert(1.0, int(cc[26]))  # 插入（insert）新的md5值
                            self.in_data_27.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_27.insert(1.0, int(cc[27]))  # 插入（insert）新的md5值
                            self.in_data_28.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_28.insert(1.0, int(cc[28]))  # 插入（insert）新的md5值
                            self.in_data_29.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_29.insert(1.0, int(cc[29]))  # 插入（insert）新的md5值

                            self.in_data_30.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_30.insert(1.0, int(cc[30]))  # 插入（insert）新的md5值
                            self.in_data_31.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_31.insert(1.0, int(cc[31]))  # 插入（insert）新的md5值
                            self.in_data_32.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_32.insert(1.0, int(cc[32]))  # 插入（insert）新的md5值
                            self.in_data_33.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_33.insert(1.0, int(cc[33]))  # 插入（insert）新的md5值
                            self.in_data_34.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_34.insert(1.0, int(cc[34]))  # 插入（insert）新的md5值
                            self.in_data_35.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_35.insert(1.0, int(cc[35]))  # 插入（insert）新的md5值
                            self.in_data_36.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_36.insert(1.0, int(cc[36]))  # 插入（insert）新的md5值
                            self.in_data_37.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_37.insert(1.0, int(cc[37]))  # 插入（insert）新的md5值
                            self.in_data_38.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_38.insert(1.0, int(cc[38]))  # 插入（insert）新的md5值
                            self.in_data_39.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_39.insert(1.0, int(cc[39]))  # 插入（insert）新的md5值

                            self.in_data_40.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_40.insert(1.0, int(cc[40]))  # 插入（insert）新的md5值
                            self.in_data_41.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_41.insert(1.0, int(cc[41]))  # 插入（insert）新的md5值
                            self.in_data_42.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_42.insert(1.0, int(cc[42]))  # 插入（insert）新的md5值
                            self.in_data_43.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_43.insert(1.0, int(cc[43]))  # 插入（insert）新的md5值
                            self.in_data_44.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_44.insert(1.0, int(cc[44]))  # 插入（insert）新的md5值
                            self.in_data_45.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_45.insert(1.0, int(cc[45]))  # 插入（insert）新的md5值
                            self.in_data_46.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_46.insert(1.0, int(cc[46]))  # 插入（insert）新的md5值
                            self.in_data_47.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_47.insert(1.0, int(cc[47]))  # 插入（insert）新的md5值
                            self.in_data_48.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_48.insert(1.0, int(cc[48]))  # 插入（insert）新的md5值
                            self.in_data_49.delete(1.0, END)  # 删除（delete）界面中原来的值
                            self.in_data_49.insert(1.0, int(cc[49]))  # 插入（insert）新的md5值

                            self.write_wendu_log("INFO:wendu_set success")  # 调用写入日志函数

                        else:
                            print('温度数据错误，处理下一组中...')
                    except:
                        print('温度数据不足')

                    self.ReceDataView.insert(INSERT, readstr)
                    self.write_rt_log("数据已接收")  # 调用写入日志函数
                    time.sleep(1)  # 接收间隔1s
                    button_pressed = 1
                print('请连接串口')
                self.write_rt_log("请连接串口")  # 调用写入日志函数  此处有个小bug，即关闭连接后，会继续运行一次此部分
            else:
                print('请先连接串口')
                self.write_rt_log("请先连接串口")  # 调用写入日志函数
        else:
            print('接收通道已打开')
            self.write_rt_log("接收通道已打开")  # 调用写入日志函数

    def button_OK_click_1(self):
        global port_opened
        if port_opened == 0:
            if self.port == None or self.port.isOpen() == False:  # 打开串口 按钮
                self.myserial.open_port(self.combobox_port.get())
                print("打开串口成功")
                self.write_rt_log("打开串口成功")  # 调用写入日志函数
                port_opened = 1
            else:
                # self.write_rt_log("打开串口失败")  # 调用写入日志函数
                pass
        else:
            print("串口已打开")
            self.write_rt_log("串口已打开")  # 调用写入日志函数

    def button_OK_click_0(self):
        print("请先选择串口")
        self.write_rt_log("请先选择串口")  # 调用写入日志函数



    def button_clcSend_click(self):  # 清除发送数据 按钮
        self.SendDataView.delete("1.0", "end")
        self.write_rt_log("发送数据已清除")  # 调用写入日志函数

    def button_clcRece_click(self):  # 清除接收数据 按钮
        self.ReceDataView.delete("1.0", "end")
        self.write_rt_log("接收数据已清除")  # 调用写入日志函数

    def button_Send_click(self):  # 发送数据 按钮
        try:
            if self.myserial.port.isOpen() == True:
                print("开始发送数据")
                self.write_rt_log("开始发送数据")  # 调用写入日志函数
                send_str1 = self.entrySend.get()
                self.myserial.Write_data(send_str1)
                self.SendDataView.insert(tkinter.INSERT, send_str1 + " ")
                print("发送数据成功")
                self.write_rt_log("数据发送成功")  # 调用写入日志函数
            else:
                print("串口没有打开")
                self.write_rt_log("串口未打开")  # 调用写入日志函数
        except:
            print("发送失败")
            self.write_rt_log("发送失败")  # 调用写入日志函数

    def button_Rece_click(self):  # 接收数据 按钮
        t = threading.Thread(target=self.Receive_Data)  # 新建线程用来不断接收数据并显示
        t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        t.start()  # 开启线程

    # 串口日志动态打印 08.20
    def write_rt_log(self, logmsg):
        global LOG_RT_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        if LOG_RT_NUM <= 3:
            self.RT_Data.insert(END, logmsg_in)
            LOG_RT_NUM = LOG_RT_NUM + 1
        else:
            self.RT_Data.delete(1.0, 2.0)  # 将之前的第1、2个数据删掉
            self.RT_Data.insert(END, logmsg_in)


def gui_start():
    init_window = Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    ZMJ_PORTAL.set_init_window()  # 设置根窗口默认属性
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


if __name__ == '__main__':
    gui_start()
