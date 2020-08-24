#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import threading  # 线程 一直接收数据，不影响主线程运行
import tkinter
from tkinter import *
from tkinter import ttk, scrolledtext
import time
import socket

LOG_LINE_NUM = 0
LOG_SE_NUM = 0
LOG_RE_NUM = 0

w1 = 8  # 上面5*10个方格的宽
h1 = 2  # 上面5*10个方格的高
x1 = [0.05 + 0.1 * i for i in range(10)]
y1 = [0.1 + 0.1 * i for i in range(5)]

w2 = 6  # 下面5*10个方格的宽
h2 = 1  # 下面5*10个方格的高
x2 = [0.05 + 0.07 * i for i in range(13)]
y2 = [0.6 + 0.05 * i for i in range(5)]

y_text = 0.85  # 下面日志框的 题标y轴
y_show = 0.93  # 下面日志框的 文本y轴

connect = 0  # 接收成功标志，默认未成功连接
num_or_col = 1  # 默认 1为温度数值显示，0为温度颜色显示
cc = 0    # 数据接收展示子函数使用
t_len = 500  # 温度数据字符串长度
num_updata_in = 500  # 内部更新函数，更新缓存间隔时间,也就是GUI页面刷新间隔
num_updata_out = 2000  # 外部更新函数，更新缓存间隔时间
hex_cc = []  # cc的hex

out_in_num_and_col = 1  # 手动设置温度数据时，1为同时使上面5*10的方框显示num和col，0为只显示col
tem_min = -50  # 显示温度下限, float型
tem_max = 100  # 显示温度上限
wendu_log_len = 50  # 左下角日志框保留文字的条数
se_log_len = 50     # 中下角日志框保留文字的条数
re_log_len = 50     # 右下角日志框保留文字的条数


class MY_GUI(object):
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    # 设置窗口  mainwin = init_window_name
    def set_init_window(self):
        global num_updata_out
        global w1, w2, h1, h2
        global x1, x2, y1, y2
        global num_or_col
        self.init_window_name.title("温度显示工具_v3.0")  # 窗口名
        self.init_window_name.geometry('1068x681+10+10')  # 290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name["bg"] = "#FFF8DC"  # 窗口背景色，其他背景色见：https://www.bejson.com/convert/rgbhex/
        self.init_window_name.attributes("-alpha", 1)  # 虚化，值越小虚化程度越高
        # self.init_window_name.iconbitmap('wen.ico')  # 会引起错误，路径找不到
        # self.init_window_name.resizable(0, 0)   # 固定屏幕尺寸
        self.sk = socket.socket()
        self.server_ip = '127.0.0.1'
        self.server_port = int(8888)
        self.recvbuf = str()  # 接收区缓存
        self.sendbuf = str()  # 发送区缓存
        # self.recvstr = StringVar(value=self.recvbuf)
        self.sendstr = StringVar(value=self.sendbuf)
        self.ip = StringVar(value=self.server_ip)
        self.port = IntVar(value=self.server_port)
        self.var = StringVar()  # 定义一个var用来将radiobutton的值和Label的值联系在一起.
        """
        自己的显示框  5*10 y=0.1-0.5
        """
        self.in_data_label = Label(self.init_window_name, text="温度显示", bg="#F8F8FF")  # 输入标签 init_data_label
        self.in_data_label.place(relx=0.05, rely=0.02, anchor=CENTER)
        # 网口标签 08.22
        self.ip_label = Label(self.init_window_name, text='IP地址', bg="#F8F8FF")
        self.ip_label.place(relx=x2[10], rely=y2[0], anchor=CENTER)
        self.port_label = Label(self.init_window_name, text='端口号', bg="#F8F8FF")
        self.port_label.place(relx=x2[10], rely=y2[1], anchor=CENTER)
        self.c_label = Label(self.init_window_name, text='输入框', bg="#F8F8FF")
        self.c_label.place(relx=x2[10], rely=y2[3], anchor=CENTER)
        # self.s_label = Label(self.init_window_name, text='当前收到', bg="#F8F8FF")
        # self.s_label.place(relx=x2[10], rely=y2[3], anchor=CENTER)
        self.secorde_label = Label(self.init_window_name, text='发送的数据', bg="#F8F8FF")
        self.secorde_label.place(relx=x2[5], rely=y_text, anchor=CENTER)
        self.recorde_label = Label(self.init_window_name, text='接收的数据', bg="#F8F8FF")
        self.recorde_label.place(relx=x2[10], rely=y_text, anchor=CENTER)
        # 网口文本框 08.22
        self.ip_entry = Entry(self.init_window_name, textvariable=self.ip)
        self.ip_entry.place(relx=x2[12], rely=y2[0], anchor=CENTER)
        self.port_entry = Entry(self.init_window_name, textvariable=self.port)
        self.port_entry.place(relx=x2[12], rely=y2[1], anchor=CENTER)
        self.c_entry = Entry(self.init_window_name, textvariable=self.sendstr)
        self.c_entry.place(relx=x2[12] - 0.05, rely=y2[2], anchor=CENTER, width=250)
        # self.s_entry = Entry(self.init_window_name, textvariable=self.recvstr, state='disabled')
        # self.s_entry.place(relx=x2[12], rely=y2[3], anchor=CENTER)
        self.secorde = scrolledtext.ScrolledText(self.init_window_name, width=40, height=6)
        self.secorde.place(relx=x2[6], rely=y_show, anchor=CENTER)
        self.recorde = scrolledtext.ScrolledText(self.init_window_name, width=40, height=6)
        self.recorde.place(relx=x2[11], rely=y_show, anchor=CENTER)

        # 网口按钮 08.22
        self.btn0 = Button(self.init_window_name, text='连接', command=lambda: self.started(self.ip, self.port),
                           bg="#FF8C00")
        self.btn0.place(relx=x2[10], rely=y2[4], anchor=CENTER)
        self.btn1 = Button(self.init_window_name, text='发送', command=lambda: self.sending(self.sk), bg="#ADFF2F")
        self.btn1.place(relx=x2[11], rely=y2[4], anchor=CENTER)
        self.in_data()
        self.out_data()
        """
        中间横线  y=0.5-0.6
        """
        self.w = Canvas(self.init_window_name, width=2000, height=10)  # 实际线宽由 height=10控制
        self.w.create_line(0, 0, 2000, 0, fill="#000000", width=30, capstyle=ROUND)  # 真实线宽 多余的被Canvas()遮挡了
        self.w.place(relx=0.5, rely=0.56, anchor=CENTER)  # Canvas上中心点位置

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
        self.wendu_data = scrolledtext.ScrolledText(self.init_window_name, width=38, height=6)  # 日志结果
        self.wendu_data.place(relx=0.155, rely=y_show, anchor=CENTER)

        # 创建2个radiobutton选项，其中variable=var, value='A'的意思就是，当我们鼠标选中了其中一个选项，把value的值A放到变量var中，然后赋值给variable
        self.chose_num = Radiobutton(self.init_window_name, text='num', variable=self.var, value=1,
                                     command=self.num_col_selection,bg='#8470FF',relief=GROOVE)
        self.chose_num.place(relx=x1[8], rely=0.03, anchor=CENTER)
        self.chose_col = Radiobutton(self.init_window_name, text='col', variable=self.var, value=0,
                                     command=self.num_col_selection,bg='#7FFFD4',relief=GROOVE)
        self.chose_col.place(relx=x1[9], rely=0.03, anchor=CENTER)
        self.var.set(num_or_col)  # 默认选择第一个

        self.init_window_name.after(num_updata_out, self.update)

    # 温度按钮 功能函数
    def wendu_trans(self):
        global num_or_col, out_in_num_and_col, tem_min, tem_max
        # print(num_or_col)
        src_00 = self.out_data_00.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        print(src_00, type(src_00), '\n', bytes.decode(src_00), type(bytes.decode(src_00)))
        src_00 = self.in_tem_or_not(src_00)
        if src_00:
            try:  # 运行正确
                if int(src_00) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_00), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_00.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_00.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_00.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_00.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_00 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_00.configure(bg=hex_00)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效00')
                        self.write_wendu_log("选择无效00")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_00.delete(1.0, END)
                self.in_data_00.insert(1.0, "温度写入失败00")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_01 = self.out_data_01.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_01 = self.in_tem_or_not(src_01)
        if src_01:
            try:  # 运行正确
                if int(src_01) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_01), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_01.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_01.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_01.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_01.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_01 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_01.configure(bg=hex_01)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效01')
                        self.write_wendu_log("选择无效01")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_01.delete(1.0, END)
                self.in_data_01.insert(1.0, "温度写入失败01")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_02 = self.out_data_02.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_02 = self.in_tem_or_not(src_02)
        if src_02:
            try:  # 运行正确
                if int(src_02) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_02), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_02.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_02.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_02.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_02.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_02 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_02.configure(bg=hex_02)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效02')
                        self.write_wendu_log("选择无效02")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_02.delete(1.0, END)
                self.in_data_02.insert(1.0, "温度写入失败02")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_03 = self.out_data_03.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_03 = self.in_tem_or_not(src_03)
        if src_03:
            try:  # 运行正确
                if int(src_03) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_03), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_03.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_03.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_03.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_03.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_03 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_03.configure(bg=hex_03)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效03')
                        self.write_wendu_log("选择无效03")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_03.delete(1.0, END)
                self.in_data_03.insert(1.0, "温度写入失败03")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_04 = self.out_data_04.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_04 = self.in_tem_or_not(src_04)
        if src_04:
            try:  # 运行正确
                if int(src_04) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_04), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_04.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_04.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_04.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_04.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_04 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_04.configure(bg=hex_04)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效04')
                        self.write_wendu_log("选择无效04")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_04.delete(1.0, END)
                self.in_data_04.insert(1.0, "温度写入失败04")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_05 = self.out_data_05.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_05 = self.in_tem_or_not(src_05)
        if src_05:
            try:  # 运行正确
                if int(src_05) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_05), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_05.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_05.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_05.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_05.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_05 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_05.configure(bg=hex_05)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效05')
                        self.write_wendu_log("选择无效05")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_05.delete(1.0, END)
                self.in_data_05.insert(1.0, "温度写入失败05")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_06 = self.out_data_06.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_06 = self.in_tem_or_not(src_06)
        if src_06:
            try:  # 运行正确
                if int(src_06) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_06), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_06.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_06.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_06.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_06.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_06 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_06.configure(bg=hex_06)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效06')
                        self.write_wendu_log("选择无效06")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_06.delete(1.0, END)
                self.in_data_06.insert(1.0, "温度写入失败06")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_07 = self.out_data_07.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_07 = self.in_tem_or_not(src_07)
        if src_07:
            try:  # 运行正确
                if int(src_07) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_07), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_07.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_07.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_07.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_07.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_07 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_07.configure(bg=hex_07)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效07')
                        self.write_wendu_log("选择无效07")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_07.delete(1.0, END)
                self.in_data_07.insert(1.0, "温度写入失败07")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_08 = self.out_data_08.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_08 = self.in_tem_or_not(src_08)
        if src_08:
            try:  # 运行正确
                if int(src_08) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_08), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_08.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_08.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_08.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_08.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_08 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_08.configure(bg=hex_08)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效08')
                        self.write_wendu_log("选择无效08")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_08.delete(1.0, END)
                self.in_data_08.insert(1.0, "温度写入失败08")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_09 = self.out_data_09.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_09 = self.in_tem_or_not(src_09)
        if src_09:
            try:  # 运行正确
                if int(src_09) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_09), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_09.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_09.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_09.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_09.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_09 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_09.configure(bg=hex_09)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效09')
                        self.write_wendu_log("选择无效09")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_09.delete(1.0, END)
                self.in_data_09.insert(1.0, "温度写入失败09")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_10 = self.out_data_10.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_10 = self.in_tem_or_not(src_10)
        if src_10:
            try:  # 运行正确
                if int(src_10) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_10), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_10.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_10.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_10.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_10.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_10 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_10.configure(bg=hex_10)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效10')
                        self.write_wendu_log("选择无效10")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_10.delete(1.0, END)
                self.in_data_10.insert(1.0, "温度写入失败10")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_11 = self.out_data_11.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_11 = self.in_tem_or_not(src_11)
        if src_11:
            try:  # 运行正确
                if int(src_11) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_11), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_11.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_11.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_11.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_11.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_11 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_11.configure(bg=hex_11)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效11')
                        self.write_wendu_log("选择无效11")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_11.delete(1.0, END)
                self.in_data_11.insert(1.0, "温度写入失败11")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_12 = self.out_data_12.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_12 = self.in_tem_or_not(src_12)
        if src_12:
            try:  # 运行正确
                if int(src_12) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_12), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_12.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_12.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_12.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_12.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_12 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_12.configure(bg=hex_12)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效12')
                        self.write_wendu_log("选择无效12")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_12.delete(1.0, END)
                self.in_data_12.insert(1.0, "温度写入失败12")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_13 = self.out_data_13.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_13 = self.in_tem_or_not(src_13)
        if src_13:
            try:  # 运行正确
                if int(src_13) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_13), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_13.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_13.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_13.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_13.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_13 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_13.configure(bg=hex_13)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效13')
                        self.write_wendu_log("选择无效13")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_13.delete(1.0, END)
                self.in_data_13.insert(1.0, "温度写入失败13")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_14 = self.out_data_14.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_14 = self.in_tem_or_not(src_14)
        if src_14:
            try:  # 运行正确
                if int(src_14) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_14), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_14.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_14.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_14.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_14.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_14 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_14.configure(bg=hex_14)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效14')
                        self.write_wendu_log("选择无效14")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_14.delete(1.0, END)
                self.in_data_14.insert(1.0, "温度写入失败14")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_15 = self.out_data_15.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_15 = self.in_tem_or_not(src_15)
        if src_15:
            try:  # 运行正确
                if int(src_15) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_15), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_15.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_15.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_15.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_15.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_15 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_15.configure(bg=hex_15)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效15')
                        self.write_wendu_log("选择无效15")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_15.delete(1.0, END)
                self.in_data_15.insert(1.0, "温度写入失败15")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_16 = self.out_data_16.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_16 = self.in_tem_or_not(src_16)
        if src_16:
            try:  # 运行正确
                if int(src_16) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_16), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_16.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_16.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_16.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_16.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_16 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_16.configure(bg=hex_16)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效16')
                        self.write_wendu_log("选择无效16")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_16.delete(1.0, END)
                self.in_data_16.insert(1.0, "温度写入失败16")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_17 = self.out_data_17.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_17 = self.in_tem_or_not(src_17)
        if src_17:
            try:  # 运行正确
                if int(src_17) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_17), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_17.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_17.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_17.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_17.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_17 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_17.configure(bg=hex_17)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效17')
                        self.write_wendu_log("选择无效17")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_17.delete(1.0, END)
                self.in_data_17.insert(1.0, "温度写入失败17")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_18 = self.out_data_18.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_18 = self.in_tem_or_not(src_18)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_18:
            try:  # 运行正确
                if int(src_18) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_18), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_18.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_18.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_18.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_18.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_18 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_18.configure(bg=hex_18)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效18')
                        self.write_wendu_log("选择无效18")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_18.delete(1.0, END)
                self.in_data_18.insert(1.0, "温度写入失败18")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_19 = self.out_data_19.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_19 = self.in_tem_or_not(src_19)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_19:
            try:  # 运行正确
                if int(src_19) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_19), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_19.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_19.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_19.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_19.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_19 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_19.configure(bg=hex_19)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效19')
                        self.write_wendu_log("选择无效19")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_19.delete(1.0, END)
                self.in_data_19.insert(1.0, "温度写入失败19")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_20 = self.out_data_20.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_20 = self.in_tem_or_not(src_20)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_20:
            try:  # 运行正确
                if int(src_20) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_20), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_20.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_20.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_20.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_20.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_20 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_20.configure(bg=hex_20)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效20')
                        self.write_wendu_log("选择无效20")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_20.delete(1.0, END)
                self.in_data_20.insert(1.0, "温度写入失败20")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_21 = self.out_data_21.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_21 = self.in_tem_or_not(src_21)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_21:
            try:  # 运行正确
                if int(src_21) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_21), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_21.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_21.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_21.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_21.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_21 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_21.configure(bg=hex_21)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效21')
                        self.write_wendu_log("选择无效21")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_21.delete(1.0, END)
                self.in_data_21.insert(1.0, "温度写入失败21")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_22 = self.out_data_22.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_22 = self.in_tem_or_not(src_22)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_22:
            try:  # 运行正确
                if int(src_22) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_22), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_22.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_22.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_22.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_22.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_22 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_22.configure(bg=hex_22)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效22')
                        self.write_wendu_log("选择无效22")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_22.delete(1.0, END)
                self.in_data_22.insert(1.0, "温度写入失败22")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_23 = self.out_data_23.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_23 = self.in_tem_or_not(src_23)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_23:
            try:  # 运行正确
                if int(src_23) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_23), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_23.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_23.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_23.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_23.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_23 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_23.configure(bg=hex_23)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效23')
                        self.write_wendu_log("选择无效23")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_23.delete(1.0, END)
                self.in_data_23.insert(1.0, "温度写入失败23")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_24 = self.out_data_24.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_24 = self.in_tem_or_not(src_24)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_24:
            try:  # 运行正确
                if int(src_24) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_24), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_24.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_24.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_24.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_24.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_24 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_24.configure(bg=hex_24)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效24')
                        self.write_wendu_log("选择无效24")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_24.delete(1.0, END)
                self.in_data_24.insert(1.0, "温度写入失败24")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_25 = self.out_data_25.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_25 = self.in_tem_or_not(src_25)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_25:
            try:  # 运行正确
                if int(src_25) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_25), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_25.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_25.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_25.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_25.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_25 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_25.configure(bg=hex_25)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效25')
                        self.write_wendu_log("选择无效25")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_25.delete(1.0, END)
                self.in_data_25.insert(1.0, "温度写入失败25")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_26 = self.out_data_26.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_26 = self.in_tem_or_not(src_26)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_26:
            try:  # 运行正确
                if int(src_26) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_26), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_26.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_26.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_26.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_26.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_26 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_26.configure(bg=hex_26)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效26')
                        self.write_wendu_log("选择无效26")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_26.delete(1.0, END)
                self.in_data_26.insert(1.0, "温度写入失败26")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_27 = self.out_data_27.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_27 = self.in_tem_or_not(src_27)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_27:
            try:  # 运行正确
                if int(src_27) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_27), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_27.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_27.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_27.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_27.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_27 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_27.configure(bg=hex_27)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效27')
                        self.write_wendu_log("选择无效27")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_27.delete(1.0, END)
                self.in_data_27.insert(1.0, "温度写入失败27")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_28 = self.out_data_28.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_28 = self.in_tem_or_not(src_28)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_28:
            try:  # 运行正确
                if int(src_28) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_28), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_28.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_28.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_28.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_28.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_28 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_28.configure(bg=hex_28)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效28')
                        self.write_wendu_log("选择无效28")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_28.delete(1.0, END)
                self.in_data_28.insert(1.0, "温度写入失败28")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_29 = self.out_data_29.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_29 = self.in_tem_or_not(src_29)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_29:
            try:  # 运行正确
                if int(src_29) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_29), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_29.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_29.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_29.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_29.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_29 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_29.configure(bg=hex_29)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效29')
                        self.write_wendu_log("选择无效29")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_29.delete(1.0, END)
                self.in_data_29.insert(1.0, "温度写入失败29")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_30 = self.out_data_30.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_30 = self.in_tem_or_not(src_30)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_30:
            try:  # 运行正确
                if int(src_30) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_30), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_30.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_30.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_30.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_30.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_30 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_30.configure(bg=hex_30)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效30')
                        self.write_wendu_log("选择无效30")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_30.delete(1.0, END)
                self.in_data_30.insert(1.0, "温度写入失败30")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_31 = self.out_data_31.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_31 = self.in_tem_or_not(src_31)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_31:
            try:  # 运行正确
                if int(src_31) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_31), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_31.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_31.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_31.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_31.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_31 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_31.configure(bg=hex_31)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效31')
                        self.write_wendu_log("选择无效31")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_31.delete(1.0, END)
                self.in_data_31.insert(1.0, "温度写入失败31")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_32 = self.out_data_32.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_32 = self.in_tem_or_not(src_32)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_32:
            try:  # 运行正确
                if int(src_32) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_32), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_32.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_32.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_32.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_32.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_32 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_32.configure(bg=hex_32)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效32')
                        self.write_wendu_log("选择无效32")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_32.delete(1.0, END)
                self.in_data_32.insert(1.0, "温度写入失败32")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_33 = self.out_data_33.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_33 = self.in_tem_or_not(src_33)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_33:
            try:  # 运行正确
                if int(src_33) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_33), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_33.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_33.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_33.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_33.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_33 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_33.configure(bg=hex_33)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效33')
                        self.write_wendu_log("选择无效33")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_33.delete(1.0, END)
                self.in_data_33.insert(1.0, "温度写入失败33")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_34 = self.out_data_34.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_34 = self.in_tem_or_not(src_34)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_34:
            try:  # 运行正确
                if int(src_34) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_34), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_34.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_34.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_34.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_34.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_34 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_34.configure(bg=hex_34)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效34')
                        self.write_wendu_log("选择无效34")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_34.delete(1.0, END)
                self.in_data_34.insert(1.0, "温度写入失败34")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_35 = self.out_data_35.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_35 = self.in_tem_or_not(src_35)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_35:
            try:  # 运行正确
                if int(src_35) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_35), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_35.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_35.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_35.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_35.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_35 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_35.configure(bg=hex_35)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效35')
                        self.write_wendu_log("选择无效35")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_35.delete(1.0, END)
                self.in_data_35.insert(1.0, "温度写入失败35")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_36 = self.out_data_36.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_36 = self.in_tem_or_not(src_36)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_36:
            try:  # 运行正确
                if int(src_36) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_36), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_36.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_36.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_36.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_36.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_36 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_36.configure(bg=hex_36)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效36')
                        self.write_wendu_log("选择无效36")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_36.delete(1.0, END)
                self.in_data_36.insert(1.0, "温度写入失败36")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_37 = self.out_data_37.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_37 = self.in_tem_or_not(src_37)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_37:
            try:  # 运行正确
                if int(src_37) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_37), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_37.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_37.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_37.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_37.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_37 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_37.configure(bg=hex_37)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效37')
                        self.write_wendu_log("选择无效37")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_37.delete(1.0, END)
                self.in_data_37.insert(1.0, "温度写入失败37")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_38 = self.out_data_38.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_38 = self.in_tem_or_not(src_38)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_38:
            try:  # 运行正确
                if int(src_38) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_38), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_38.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_38.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_38.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_38.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_38 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_38.configure(bg=hex_38)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效38')
                        self.write_wendu_log("选择无效38")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_38.delete(1.0, END)
                self.in_data_38.insert(1.0, "温度写入失败38")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_39 = self.out_data_39.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_39 = self.in_tem_or_not(src_39)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_39:
            try:  # 运行正确
                if int(src_39) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_39), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_39.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_39.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_39.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_39.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_39 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_39.configure(bg=hex_39)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效39')
                        self.write_wendu_log("选择无效39")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_39.delete(1.0, END)
                self.in_data_39.insert(1.0, "温度写入失败39")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_40 = self.out_data_40.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_40 = self.in_tem_or_not(src_40)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_40:
            try:  # 运行正确
                if int(src_40) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_40), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_40.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_40.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_40.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_40.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_40 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_40.configure(bg=hex_40)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效40')
                        self.write_wendu_log("选择无效40")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_40.delete(1.0, END)
                self.in_data_40.insert(1.0, "温度写入失败40")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_41 = self.out_data_41.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_41 = self.in_tem_or_not(src_41)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_41:
            try:  # 运行正确
                if int(src_41) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_41), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_41.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_41.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_41.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_41.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_41 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_41.configure(bg=hex_41)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效41')
                        self.write_wendu_log("选择无效41")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_41.delete(1.0, END)
                self.in_data_41.insert(1.0, "温度写入失败41")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_42 = self.out_data_42.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_42 = self.in_tem_or_not(src_42)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_42:
            try:  # 运行正确
                if int(src_42) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_42), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_42.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_42.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_42.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_42.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_42 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_42.configure(bg=hex_42)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效42')
                        self.write_wendu_log("选择无效42")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_42.delete(1.0, END)
                self.in_data_42.insert(1.0, "温度写入失败42")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_43 = self.out_data_43.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_43 = self.in_tem_or_not(src_43)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_43:
            try:  # 运行正确
                if int(src_43) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_43), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_43.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_43.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_43.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_43.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_43 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_43.configure(bg=hex_43)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效43')
                        self.write_wendu_log("选择无效43")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_43.delete(1.0, END)
                self.in_data_43.insert(1.0, "温度写入失败43")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_44 = self.out_data_44.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_44 = self.in_tem_or_not(src_44)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_44:
            try:  # 运行正确
                if int(src_44) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_44), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_44.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_44.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_44.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_44.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_44 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_44.configure(bg=hex_44)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效44')
                        self.write_wendu_log("选择无效44")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_44.delete(1.0, END)
                self.in_data_44.insert(1.0, "温度写入失败44")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_45 = self.out_data_45.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_45 = self.in_tem_or_not(src_45)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_45:
            try:  # 运行正确
                if int(src_45) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_45), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_45.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_45.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_45.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_45.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_45 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_45.configure(bg=hex_45)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效45')
                        self.write_wendu_log("选择无效45")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_45.delete(1.0, END)
                self.in_data_45.insert(1.0, "温度写入失败45")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_46 = self.out_data_46.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_46 = self.in_tem_or_not(src_46)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_46:
            try:  # 运行正确
                if int(src_46) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_46), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_46.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_46.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_46.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_46.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_46 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_46.configure(bg=hex_46)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效46')
                        self.write_wendu_log("选择无效46")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_46.delete(1.0, END)
                self.in_data_46.insert(1.0, "温度写入失败46")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_47 = self.out_data_47.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_47 = self.in_tem_or_not(src_47)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_47:
            try:  # 运行正确
                if int(src_47) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_47), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_47.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_47.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_47.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_47.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_47 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_47.configure(bg=hex_47)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效47')
                        self.write_wendu_log("选择无效47")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_47.delete(1.0, END)
                self.in_data_47.insert(1.0, "温度写入失败47")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_48 = self.out_data_48.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_48 = self.in_tem_or_not(src_48)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_48:
            try:  # 运行正确
                if int(src_48) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_48), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_48.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_48.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_48.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_48.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_48 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_48.configure(bg=hex_48)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效48')
                        self.write_wendu_log("选择无效48")  # 调用写入日志函数
            except:  # 运行出错
                self.in_data_48.delete(1.0, END)
                self.in_data_48.insert(1.0, "温度写入失败48")
        else:  # 没数据输入
            self.write_wendu_log("ERROR:wendu_set failed")

        src_49 = self.out_data_49.get(1.0, END).strip().replace("\n", "").encode()  # 获取所有（get）录入框中的字符
        src_49 = self.in_tem_or_not(src_49)  # 正确就正确，空为666666，值不对为bgdnuidxv
        if src_49:
            try:  # 运行正确
                if int(src_49) == 666666:
                    pass
                else:
                    wendu_num = round(float(src_49), 1)  # 保留一位小数
                    print(wendu_num)
                    if int(num_or_col) == 1:
                        self.set_bg_num()  # 设置所有背景为白色
                        self.in_data_49.delete(1.0, END)  # 删除（delete）界面中原来的值
                        self.in_data_49.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        self.write_wendu_log("INFO:wendu_num success")  # 调用写入日志函数
                    elif int(num_or_col) == 0:
                        self.in_data_49.delete(1.0, END)  # 删除（delete）界面中原来的值
                        if out_in_num_and_col == 1:  # num 和 col 都要
                            self.in_data_49.insert(1.0, wendu_num)  # 插入（insert）新的md5值
                        else:
                            pass
                        hex_49 = self.num_trans_col(wendu_num)  # 求hex
                        self.in_data_49.configure(bg=hex_49)  # 上色
                        self.write_wendu_log("INFO:wendu_col success")  # 调用写入日志函数
                    else:
                        print('选择无效49')
                        self.write_wendu_log("选择无效49")  # 调用写入日志函数
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
        global LOG_LINE_NUM, wendu_log_len
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        if LOG_LINE_NUM <= wendu_log_len:
            self.wendu_data.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.wendu_data.delete(1.0, 2.0)  # 将之前的第1、2个数据删掉
            self.wendu_data.insert(END, logmsg_in)

    """串口部分 2020.08.19 https://www.cnblogs.com/zhicungaoyuan-mingzhi/p/12303229.html"""

    # 定义选项触发函数功能
    def num_col_selection(self):
        global num_or_col
        num_or_col = self.var.get()
        print(num_or_col)

    # 开始连接 并在日志框显示
    def started(self, ip, port):
        global connect
        if connect == 0:
            self.wendu_data.insert(INSERT, 'waiting...\n')  # 文本展示区 展示
            self.sk.connect((self.server_ip, self.server_port))  # socket连接
            print('连接成功')
            connect = 1
            self.write_wendu_log('连接成功!')  # 文本展示区 展示
        else:
            print('已连接')
            self.write_wendu_log('已连接')  # 文本展示区 展示
        return

    # 发送数据
    def senddata(self, s):
        self.sendbuf = self.sendstr.get()  # 获取发送端口写下的数据
        s.send(bytes(self.sendbuf, 'utf8'))  # 通过网口进行发送
        # self.secorde.insert(INSERT, time.strftime('%m-%d %H:%M:%S') + ' ' + self.sendbuf + '\n')  # 文本展示区 展示
        self.write_se_log(self.sendbuf)
        self.write_wendu_log('数据已发送')
        print('数据已发送')
        return

    # 接收数据 并展现在上面50个方框中
    def recvdata(self, s):
        global num_or_col, h1, cc, t_len, hex_cc, tem_min, tem_max
        print(num_or_col)
        try:
            self.recvbuf = str(s.recv(t_len), 'utf8')  # 提取出接收到的数据
            readstr = self.recvbuf
            print('num_re', readstr, type(readstr))
            if not self.recvbuf:  # 如果没接收到数据
                pass
            # 数据分割
            else:  # 有数据
                c = re.compile(r'(\s*[-]?[\d]+[.]?[\d]{0,5}\s*)')  # 至少1个数字 + 0或者1个小数点 + 任意个数字 (前后可以有空格)  可以为-
                c1 = re.compile(
                    r'a(\s*[-]?[\d]+[.]?[\d]{0,5}\s*)b')  # 校验第5个测量的温度 数据格式a23.23b，其中a和b之间的23.23为第五个温度数据 可以为-
                c2 = re.compile(
                    r'c(\s*[-]?[\d]+[.]?[\d]{0,5}\s*)d')  # 校验第5个测量的温度 数据格式c23.23d，其中a和b之间的23.23为第十个温度数据 可以为-
                cc = c.findall(readstr)
                cc1 = c1.findall(readstr)
                cc2 = c2.findall(readstr)
                list_int_cc = list(map(float, cc))
                print(cc, cc1, cc2, list_int_cc)
                if max(list_int_cc) > tem_max:
                    self.write_wendu_log("温度过大，正在准备接收下一组...")  # 调用写入日志函数
                if min(list_int_cc) < tem_min:
                    self.write_wendu_log("温度过小，正在准备接收下一组...")  # 调用写入日志函数
                else:
                    try:
                        if float(cc1[0]) == float(cc[4]) and float(cc2[0]) == float(cc[9]):  # 数据校验，是否丢失和错位
                            print('cc right')  # 数据正确，将每个数据放在对应的框里
                            if int(num_or_col) == 1:  # 选择为 num
                                print('以数字展示温度')
                                self.write_wendu_log("以数字展示温度")  # 调用写入日志函数
                                self.set_bg_num()  # 设置所有背景为白色
                                self.in_data_num()  # 上面框框写上数字
                                self.write_wendu_log("接收数据已数字显示")  # 调用写入日志函数
                            elif int(num_or_col) == 0:  # 选择为 col
                                print('以颜色展示温度')
                                self.write_wendu_log("以颜色展示温度")  # 调用写入日志函数

                                for x in range(len(cc)):
                                    hex_c = self.num_trans_col(cc[x])
                                    hex_cc.append(hex_c)
                                print(hex_cc, len(hex_cc))

                                self.show_col()  # 上面框框展示颜色
                                self.in_data_num()  # 上面框框写上数字
                                hex_cc = []  # 清零

                                self.write_wendu_log("接收数据已颜色显示")  # 调用写入日志函数
                            else:
                                print('选择无效')
                                self.write_wendu_log("选择无效")  # 调用写入日志函数
                        else:
                            print('温度数据错误，处理下一组中...')
                    except:
                        hex_cc = []  # 清零，即使出错也要清零，迎接下一组数据
                        print('温度数据不足')
                self.write_re_log(self.recvbuf)  # 文本展示区 展示
        except Exception as e:
            print('err', e)
        return

    # 对senddata()和recvdata()方法采用多线程
    def sending(self, s):
        t = threading.Thread(target=self.senddata, args=(s,))
        t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        t.start()  # 开启线程
        return

    def recving(self, s):
        t = threading.Thread(target=self.recvdata, args=(s,))
        t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        t.start()  # 开启线程
        return

    # 更新缓存区
    def update(self):
        global num_updata_in
        try:
            self.recving(self.sk)  # 接收数据
        except Exception as e:
            print(e)
        self.init_window_name.after(num_updata_in, self.update)
        return

    # 温度数字转颜色
    def num_trans_col(self, num):
        global tem_min, tem_max
        t_num = abs(float(num) - float(tem_min))  # 温度进行了内部改变
        weight = round(255 * t_num / (abs(tem_max - tem_min)))  # [-50,100]的温度转换成0-255范围,权重取整
        col_r = abs(0 - weight)
        col_g = abs(0 - weight)
        col_b = abs(255 - weight)
        hex = "#%02x%02x%02x" % (col_r, col_g, col_b)
        return hex

    # 温度发送动态打印
    def write_se_log(self, logmsg):
        global LOG_SE_NUM, se_log_len
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        if LOG_SE_NUM <= se_log_len:
            self.secorde.insert(END, logmsg_in)
            LOG_SE_NUM = LOG_SE_NUM + 1
        else:
            self.secorde.delete(1.0, 2.0)  # 将之前的第1、2个数据删掉
            self.secorde.insert(END, logmsg_in)

    # 温度接收动态打印
    def write_re_log(self, logmsg):
        global LOG_RE_NUM, re_log_len
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        if LOG_RE_NUM <= re_log_len:
            self.recorde.insert(END, logmsg_in)
            LOG_RE_NUM = LOG_RE_NUM + 1
        else:
            self.recorde.delete(1.0, 2.0)  # 将之前的第1、2个数据删掉
            self.recorde.insert(END, logmsg_in)

    # 下设置上，判断数值是否超出范围
    def in_tem_or_not(self, src):
        global tem_min, tem_max
        try:
            src = float(bytes.decode(src))
            # print('111',src, type(src),src==None)
            if src == '':
                src = 666666
            elif tem_min <= float(src) <= tem_max:
                src = src
            else:
                src = 'bgdnuidxb'
            return src
        except:
            self.write_wendu_log("ERROR:in_tem_or_not")
            print('ERROR:in_tem_or_not')


    # 设置所有背景为白色
    def set_bg_num(self):
        self.in_data_00.configure(bg='#FFFFFF')
        self.in_data_01.configure(bg='#FFFFFF')
        self.in_data_02.configure(bg='#FFFFFF')
        self.in_data_03.configure(bg='#FFFFFF')
        self.in_data_04.configure(bg='#FFFFFF')
        self.in_data_05.configure(bg='#FFFFFF')
        self.in_data_06.configure(bg='#FFFFFF')
        self.in_data_07.configure(bg='#FFFFFF')
        self.in_data_08.configure(bg='#FFFFFF')
        self.in_data_09.configure(bg='#FFFFFF')

        self.in_data_10.configure(bg='#FFFFFF')
        self.in_data_11.configure(bg='#FFFFFF')
        self.in_data_12.configure(bg='#FFFFFF')
        self.in_data_13.configure(bg='#FFFFFF')
        self.in_data_14.configure(bg='#FFFFFF')
        self.in_data_15.configure(bg='#FFFFFF')
        self.in_data_16.configure(bg='#FFFFFF')
        self.in_data_17.configure(bg='#FFFFFF')
        self.in_data_18.configure(bg='#FFFFFF')
        self.in_data_19.configure(bg='#FFFFFF')

        self.in_data_20.configure(bg='#FFFFFF')
        self.in_data_21.configure(bg='#FFFFFF')
        self.in_data_22.configure(bg='#FFFFFF')
        self.in_data_23.configure(bg='#FFFFFF')
        self.in_data_24.configure(bg='#FFFFFF')
        self.in_data_25.configure(bg='#FFFFFF')
        self.in_data_26.configure(bg='#FFFFFF')
        self.in_data_27.configure(bg='#FFFFFF')
        self.in_data_28.configure(bg='#FFFFFF')
        self.in_data_29.configure(bg='#FFFFFF')

        self.in_data_30.configure(bg='#FFFFFF')
        self.in_data_31.configure(bg='#FFFFFF')
        self.in_data_32.configure(bg='#FFFFFF')
        self.in_data_33.configure(bg='#FFFFFF')
        self.in_data_34.configure(bg='#FFFFFF')
        self.in_data_35.configure(bg='#FFFFFF')
        self.in_data_36.configure(bg='#FFFFFF')
        self.in_data_37.configure(bg='#FFFFFF')
        self.in_data_38.configure(bg='#FFFFFF')
        self.in_data_39.configure(bg='#FFFFFF')

        self.in_data_40.configure(bg='#FFFFFF')
        self.in_data_41.configure(bg='#FFFFFF')
        self.in_data_42.configure(bg='#FFFFFF')
        self.in_data_43.configure(bg='#FFFFFF')
        self.in_data_44.configure(bg='#FFFFFF')
        self.in_data_45.configure(bg='#FFFFFF')
        self.in_data_46.configure(bg='#FFFFFF')
        self.in_data_47.configure(bg='#FFFFFF')
        self.in_data_48.configure(bg='#FFFFFF')
        self.in_data_49.configure(bg='#FFFFFF')

    # 设置上面50个框
    def in_data(self):
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

    # 设置下面50个框
    def out_data(self):
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

    # 设置下转上温度数值显示
    def in_data_num(self):
        global cc
        self.in_data_00.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_00.insert(1.0, str(float(cc[0])) + '°C')  # 插入（insert）新的md5值
        self.in_data_01.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_01.insert(1.0, str(float(cc[1])) + '°C')  # 插入（insert）新的md5值
        self.in_data_02.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_02.insert(1.0, str(float(cc[2])) + '°C')  # 插入（insert）新的md5值
        self.in_data_03.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_03.insert(1.0, str(float(cc[3])) + '°C')  # 插入（insert）新的md5值
        self.in_data_04.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_04.insert(1.0, str(float(cc[4])) + '°C')  # 插入（insert）新的md5值
        self.in_data_05.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_05.insert(1.0, str(float(cc[5])) + '°C')  # 插入（insert）新的md5值
        self.in_data_06.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_06.insert(1.0, str(float(cc[6])) + '°C')  # 插入（insert）新的md5值
        self.in_data_07.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_07.insert(1.0, str(float(cc[7])) + '°C')  # 插入（insert）新的md5值
        self.in_data_08.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_08.insert(1.0, str(float(cc[8])) + '°C')  # 插入（insert）新的md5值
        self.in_data_09.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_09.insert(1.0, str(float(cc[9])) + '°C')  # 插入（insert）新的md5值

        self.in_data_10.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_10.insert(1.0, float(cc[10]))  # 插入（insert）新的md5值
        self.in_data_11.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_11.insert(1.0, float(cc[11]))  # 插入（insert）新的md5值
        self.in_data_12.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_12.insert(1.0, float(cc[12]))  # 插入（insert）新的md5值
        self.in_data_13.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_13.insert(1.0, float(cc[13]))  # 插入（insert）新的md5值
        self.in_data_14.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_14.insert(1.0, float(cc[14]))  # 插入（insert）新的md5值
        self.in_data_15.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_15.insert(1.0, float(cc[15]))  # 插入（insert）新的md5值
        self.in_data_16.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_16.insert(1.0, float(cc[16]))  # 插入（insert）新的md5值
        self.in_data_17.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_17.insert(1.0, float(cc[17]))  # 插入（insert）新的md5值
        self.in_data_18.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_18.insert(1.0, float(cc[18]))  # 插入（insert）新的md5值
        self.in_data_19.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_19.insert(1.0, float(cc[19]))  # 插入（insert）新的md5值

        self.in_data_20.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_20.insert(1.0, float(cc[20]))  # 插入（insert）新的md5值
        self.in_data_21.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_21.insert(1.0, float(cc[21]))  # 插入（insert）新的md5值
        self.in_data_22.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_22.insert(1.0, float(cc[22]))  # 插入（insert）新的md5值
        self.in_data_23.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_23.insert(1.0, float(cc[23]))  # 插入（insert）新的md5值
        self.in_data_24.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_24.insert(1.0, float(cc[24]))  # 插入（insert）新的md5值
        self.in_data_25.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_25.insert(1.0, float(cc[25]))  # 插入（insert）新的md5值
        self.in_data_26.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_26.insert(1.0, float(cc[26]))  # 插入（insert）新的md5值
        self.in_data_27.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_27.insert(1.0, float(cc[27]))  # 插入（insert）新的md5值
        self.in_data_28.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_28.insert(1.0, float(cc[28]))  # 插入（insert）新的md5值
        self.in_data_29.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_29.insert(1.0, float(cc[29]))  # 插入（insert）新的md5值

        self.in_data_30.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_30.insert(1.0, float(cc[30]))  # 插入（insert）新的md5值
        self.in_data_31.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_31.insert(1.0, float(cc[31]))  # 插入（insert）新的md5值
        self.in_data_32.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_32.insert(1.0, float(cc[32]))  # 插入（insert）新的md5值
        self.in_data_33.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_33.insert(1.0, float(cc[33]))  # 插入（insert）新的md5值
        self.in_data_34.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_34.insert(1.0, float(cc[34]))  # 插入（insert）新的md5值
        self.in_data_35.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_35.insert(1.0, float(cc[35]))  # 插入（insert）新的md5值
        self.in_data_36.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_36.insert(1.0, float(cc[36]))  # 插入（insert）新的md5值
        self.in_data_37.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_37.insert(1.0, float(cc[37]))  # 插入（insert）新的md5值
        self.in_data_38.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_38.insert(1.0, float(cc[38]))  # 插入（insert）新的md5值
        self.in_data_39.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_39.insert(1.0, float(cc[39]))  # 插入（insert）新的md5值

        self.in_data_40.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_40.insert(1.0, float(cc[40]))  # 插入（insert）新的md5值
        self.in_data_41.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_41.insert(1.0, float(cc[41]))  # 插入（insert）新的md5值
        self.in_data_42.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_42.insert(1.0, float(cc[42]))  # 插入（insert）新的md5值
        self.in_data_43.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_43.insert(1.0, float(cc[43]))  # 插入（insert）新的md5值
        self.in_data_44.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_44.insert(1.0, float(cc[44]))  # 插入（insert）新的md5值
        self.in_data_45.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_45.insert(1.0, float(cc[45]))  # 插入（insert）新的md5值
        self.in_data_46.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_46.insert(1.0, float(cc[46]))  # 插入（insert）新的md5值
        self.in_data_47.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_47.insert(1.0, float(cc[47]))  # 插入（insert）新的md5值
        self.in_data_48.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_48.insert(1.0, float(cc[48]))  # 插入（insert）新的md5值
        self.in_data_49.delete(1.0, END)  # 删除（delete）界面中原来的值
        self.in_data_49.insert(1.0, float(cc[49]))  # 插入（insert）新的md5值

    # 设置改变上面5*10的背景颜色
    def show_col(self):
        global hex_cc
        self.in_data_00.configure(bg=hex_cc[0])
        self.in_data_01.configure(bg=hex_cc[1])
        self.in_data_02.configure(bg=hex_cc[2])
        self.in_data_03.configure(bg=hex_cc[3])
        self.in_data_04.configure(bg=hex_cc[4])
        self.in_data_05.configure(bg=hex_cc[5])
        self.in_data_06.configure(bg=hex_cc[6])
        self.in_data_07.configure(bg=hex_cc[7])
        self.in_data_08.configure(bg=hex_cc[8])
        self.in_data_09.configure(bg=hex_cc[9])

        self.in_data_10.configure(bg=hex_cc[10])
        self.in_data_11.configure(bg=hex_cc[11])
        self.in_data_12.configure(bg=hex_cc[12])
        self.in_data_13.configure(bg=hex_cc[13])
        self.in_data_14.configure(bg=hex_cc[14])
        self.in_data_15.configure(bg=hex_cc[15])
        self.in_data_16.configure(bg=hex_cc[16])
        self.in_data_17.configure(bg=hex_cc[17])
        self.in_data_18.configure(bg=hex_cc[18])
        self.in_data_19.configure(bg=hex_cc[19])

        self.in_data_20.configure(bg=hex_cc[20])
        self.in_data_21.configure(bg=hex_cc[21])
        self.in_data_22.configure(bg=hex_cc[22])
        self.in_data_23.configure(bg=hex_cc[23])
        self.in_data_24.configure(bg=hex_cc[24])
        self.in_data_25.configure(bg=hex_cc[25])
        self.in_data_26.configure(bg=hex_cc[26])
        self.in_data_27.configure(bg=hex_cc[27])
        self.in_data_28.configure(bg=hex_cc[28])
        self.in_data_29.configure(bg=hex_cc[29])

        self.in_data_30.configure(bg=hex_cc[30])
        self.in_data_31.configure(bg=hex_cc[31])
        self.in_data_32.configure(bg=hex_cc[32])
        self.in_data_33.configure(bg=hex_cc[33])
        self.in_data_34.configure(bg=hex_cc[34])
        self.in_data_35.configure(bg=hex_cc[35])
        self.in_data_36.configure(bg=hex_cc[36])
        self.in_data_37.configure(bg=hex_cc[37])
        self.in_data_38.configure(bg=hex_cc[38])
        self.in_data_39.configure(bg=hex_cc[39])

        self.in_data_40.configure(bg=hex_cc[40])
        self.in_data_41.configure(bg=hex_cc[41])
        self.in_data_42.configure(bg=hex_cc[42])
        self.in_data_43.configure(bg=hex_cc[43])
        self.in_data_44.configure(bg=hex_cc[44])
        self.in_data_45.configure(bg=hex_cc[45])
        self.in_data_46.configure(bg=hex_cc[46])
        self.in_data_47.configure(bg=hex_cc[47])
        self.in_data_48.configure(bg=hex_cc[48])
        self.in_data_49.configure(bg=hex_cc[49])


def gui_start():
    init_window = Tk()  # 实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    ZMJ_PORTAL.set_init_window()  # 设置根窗口默认属性
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


if __name__ == '__main__':
    gui_start()
