#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading  # 线程 一直接收数据，不影响主线程运行
import tkinter
from tkinter import *
from tkinter import ttk, scrolledtext
import tkinter.font as tkFont
import time
import socket
import re
from functools import reduce
import random

LOG_LINE_NUM = 0
LOG_SE_NUM = 0
LOG_RE_NUM = 0

w1 = 6  # 上面5*10个方格的宽
h1 = 1  # 上面5*10个方格的高
x1 = [0.05 + 0.1 * i for i in range(10)]
y1 = [0.05 + 0.07 * i for i in range(10)]

w2 = 6  # 下面5*10个方格的宽
h2 = 1  # 下面5*10个方格的高
x2 = [0.05 + 0.07 * i for i in range(13)]
y2 = [0.45 + 0.05 * i for i in range(5)]

x3 = [0.05 + 0.1 * i for i in range(10)]
y3 = [0.1 + 0.1 * i for i in range(7)]

y_text = 0.75  # 下面日志框的 题标y轴
y_show = 0.87  # 下面日志框的 文本y轴

connect = 0  # 接收成功标志，默认未成功连接
hot_or_col = 0  # 默认 1为温度数值显示，0为温度颜色显示
cc = 0  # 数据接收展示子函数使用
t_len = 500  # 温度数据字符串长度
num_updata_in = 500  # 内部更新函数，更新缓存间隔时间,也就是GUI页面刷新间隔
num_updata_out = 2000  # 外部更新函数，更新缓存间隔时间
hex_cc = []  # cc的hex

out_in_num_and_col = 1  # 手动设置温度数据时，1为同时使上面5*10的方框显示num和col，0为只显示col
tem_min = -50  # 显示温度下限, float型
tem_max = 100  # 显示温度上限
wendu_log_len = 50  # 左下角日志框保留文字的条数
se_log_len = 50  # 中下角日志框保留文字的条数
re_log_len = 50  # 右下角日志框保留文字的条数

ziti = "仿宋"
zihao = 12

times_threading = 0
readstr = 0
get_data_4hex_huan = '0'
t1 = 0


class FATHER(tkinter.Tk):
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name

    # 设置窗口  mainwin = init_window_name
    def set_father_window(self):
        global num_updata_out
        global w1, w2, h1, h2
        global x1, x2, y1, y2, t
        global hot_or_col, times_threading
        self.init_window_name.title("温度监控")  # 窗口名
        self.init_window_name.geometry('1068x681+700+10')  # 290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name["bg"] = "#FFF8DC"  # 窗口背景色，其他背景色见：https://www.bejson.com/convert/rgbhex/
        self.init_window_name.attributes("-alpha", 1)  # 虚化，值越小虚化程度越高
        # self.init_window_name.iconbitmap('wen.ico')  # 会引起错误，路径找不到
        # self.init_window_name.resizable(0, 0)   # 固定屏幕尺寸
        self.sk = socket.socket()
        # self.server_ip = '192.168.3.26'
        # self.server_port = int(6688)
        self.server_ip = '192.168.0.16'
        self.server_port = int(20108)
        self.ip = StringVar(value=self.server_ip)
        self.port = IntVar(value=self.server_port)
        self.recvbuf = str()  # 接收区缓存
        #  发送缓存
        self.sendbuf = str()  # 发送区缓存
        self.sendAllBuff = str()  # 总发送区缓存
        self.send0Buff = str()  # 0路发送区缓存
        self.send1Buff = str()  # 1路发送区缓存
        self.send2Buff = str()  # 2路发送区缓存
        self.send3Buff = str()  # 3路发送区缓存
        self.send4Buff = str()  # 4路发送区缓存
        self.send5Buff = str()  # 5路发送区缓存
        self.send6Buff = str()  # 6路发送区缓存
        self.send7Buff = str()  # 7路发送区缓存
        self.send8Buff = str()  # 8路发送区缓存
        self.send9Buff = str()  # 9路发送区缓存

        #  发送内容
        self.sendAllSet = StringVar(value=self.sendAllBuff)
        # self.sendstr = StringVar(value=self.sendbuf)
        self.sendSet_0 = StringVar(value=self.send0Buff)
        self.sendSet_1 = StringVar(value=self.send1Buff)
        self.sendSet_2 = StringVar(value=self.send2Buff)
        self.sendSet_3 = StringVar(value=self.send3Buff)
        self.sendSet_4 = StringVar(value=self.send4Buff)
        self.sendSet_5 = StringVar(value=self.send5Buff)
        self.sendSet_6 = StringVar(value=self.send6Buff)
        self.sendSet_7 = StringVar(value=self.send7Buff)
        self.sendSet_8 = StringVar(value=self.send8Buff)
        self.sendSet_9 = StringVar(value=self.send9Buff)

        self.avg_num = StringVar()  #
        self.env_num = StringVar()
        self.avg_num_0 = StringVar()  #
        self.avg_num_1 = StringVar()
        self.avg_num_2 = StringVar()
        self.avg_num_3 = StringVar()
        self.avg_num_4 = StringVar()
        self.avg_num_5 = StringVar()
        self.avg_num_6 = StringVar()
        self.avg_num_7 = StringVar()
        self.avg_num_8 = StringVar()
        self.avg_num_9 = StringVar()

        self.var = StringVar()  # 定义一个var用来将radiobutton的值和Label的值联系在一起.

        self.wendu_label = Label(self.init_window_name, text="温度设置结果", bg="#F0FFFF", font=("仿宋", 12))  # 日志标签 log_label
        self.wendu_label.place(relx=0.05, rely=y_text, anchor=CENTER)
        self.secorde_label = Label(self.init_window_name, text='已发送的数据', bg="#F0FFFF", font=("仿宋", 12))
        self.secorde_label.place(relx=x2[5] - 0.02, rely=y_text, anchor=CENTER)
        self.recorde_label = Label(self.init_window_name, text='已接收的数据', bg="#F0FFFF", font=("仿宋", 12))
        self.recorde_label.place(relx=x2[10] - 0.02, rely=y_text, anchor=CENTER)

        # # 待发送的数据 08.22
        # self.c_entry = Entry(self.init_window_name, textvariable=self.sendstr)
        # self.c_entry.place(relx=x2[12] - 0.05, rely=y2[2], anchor=CENTER, width=60)

        self.wendu_data = scrolledtext.ScrolledText(self.init_window_name, width=38, height=9)  # 日志结果
        self.wendu_data.place(relx=0.155, rely=y_show, anchor=CENTER)
        self.secorde = scrolledtext.ScrolledText(self.init_window_name, width=40, height=9)  # 发送结果
        self.secorde.place(relx=x2[6], rely=y_show, anchor=CENTER)
        self.recorde = scrolledtext.ScrolledText(self.init_window_name, width=40, height=9)  # 接收结果
        self.recorde.place(relx=x2[11], rely=y_show, anchor=CENTER)

        # 网口按钮 08.22
        self.btn0 = Button(self.init_window_name, text='连接', command=lambda: self.started(self.ip, self.port),
                           bg="#ADFF2F", cursor='hand2')
        self.btn0.place(relx=x1[8] + 0.06, rely=y1[0], anchor=CENTER)
        self.btn1 = Button(self.init_window_name, text='断开', command=lambda: self.closed(), bg="#FF0000",
                           cursor='hand2')
        self.btn1.place(relx=x1[9], rely=y1[0], anchor=CENTER)

        # 日志清除按钮
        # self.btn2 = Button(self.init_window_name, text='清除1', command=lambda: self.wendu_data.delete(1.0, END),
        #                    bg="#ADFF2F", cursor='hand2', font=("仿宋", 9))
        # self.btn2.place(relx=0.27, rely=0.85, anchor=CENTER)
        # self.btn3 = Button(self.init_window_name, text='清除2', command=lambda: self.secorde.delete(1.0, END),
        #                    bg="#ADFF2F", cursor='hand2', font=("仿宋", 9))
        # self.btn3.place(relx=0.59, rely=0.85, anchor=CENTER)
        # self.btn4 = Button(self.init_window_name, text='清除3', command=lambda: self.recorde.delete(1.0, END),
        #                    bg="#ADFF2F", cursor='hand2', font=("仿宋", 9))
        # self.btn4.place(relx=0.94, rely=0.85, anchor=CENTER)

        # 温度设置标签

        # self.sk.connect((self.server_ip, self.server_port))  # socket连接
        self.init_window_name.after(num_updata_out, self.update)  # 直接接收数据
        self.setLine1()  # 中间横线  y=0.5-0.6
        self.setLine2()  # 中间横线  y=0.5-0.6
        self.all_env()  # 平均温度和环境温度
        self.all_set()  # 整体温度设置
        # self.ten_avg()  # 10路平均温度
        self.ten_set()  # 局部温度设置
        self.hot_col()  # 选项触发函数

    # 定义选项触发函数
    def hot_col(self):
        global hot_or_col
        # 创建2个radiobutton选项，其中variable=var, value='A'的意思就是，当我们鼠标选中了其中一个选项，把value的值A放到变量var中，然后赋值给variable
        self.chose_hot = Radiobutton(self.init_window_name, text='制热', variable=self.var, value=1,
                                     command=self.hot_col_selection, bg='#FF3030', relief=GROOVE, width=4,
                                     cursor='hand2')
        self.chose_hot.place(relx=x1[9] - 0.05, rely=y1[3] - 0.04, anchor=CENTER)
        self.chose_col = Radiobutton(self.init_window_name, text='制冷', variable=self.var, value=0,
                                     command=self.hot_col_selection, bg='#7FFFD4', relief=GROOVE, width=4,
                                     cursor='hand2')
        self.chose_col.place(relx=x1[9] - 0.05, rely=y1[3], anchor=CENTER)
        self.var.set(hot_or_col)  # 默认选择第一个

    # 定义选项触发函数功能
    def hot_col_selection(self):
        global hot_or_col
        hot_or_col = self.var.get()

    # 开始连接 并在日志框显示
    def started(self, ip, port):
        global connect, get_data_31_old, t_set, avg_num_sum  # 初始化参数
        t_set = -100  # 初始化温度手动设置数值
        avg_num_sum = -200  # 初始化温度,手动设置数值
        if connect == 0:
            self.sk = socket.socket()
            self.wendu_data.insert(INSERT, 'waiting...\n')  # 文本展示区 展示
            self.sk.connect((self.server_ip, self.server_port))  # socket连接
            print('连接成功')
            connect = 1
            get_data_31_old = ([-200] * 30, 0)  # 初始化get_data_31_old
            self.write_wendu_log('连接成功!')  # 文本展示区 展示
        else:
            print('已连接')
            self.write_wendu_log('已连接')  # 文本展示区 展示

    # 关闭连接 并在日志框显示
    def closed(self):
        global connect
        if connect == 1:
            self.wendu_data.insert(INSERT, 'waiting...\n')  # 文本展示区 展示
            self.sk.close()  # socket连接
            print('关闭成功')
            connect = 0
            self.write_wendu_log('关闭成功!')  # 文本展示区 展示
        else:
            print('已关闭')
            self.write_wendu_log('已关闭')  # 文本展示区 展示
        return

    # 中间横线
    def setLine1(self):
        self.w = Canvas(self.init_window_name, width=2000, height=10)  # 实际线宽由 height=10控制
        self.w.create_line(0, 0, 2000, 0, fill="#000000", width=30, capstyle=ROUND)  # 真实线宽 多余的被Canvas()遮挡了
        self.w.place(relx=0.5, rely=0.34, anchor=CENTER)  # Canvas上中心点位置

    def setLine2(self):
        self.w = Canvas(self.init_window_name, width=2000, height=10)  # 实际线宽由 height=10控制
        self.w.create_line(0, 0, 2000, 0, fill="#000000", width=30, capstyle=ROUND)  # 真实线宽 多余的被Canvas()遮挡了
        self.w.place(relx=0.5, rely=0.70, anchor=CENTER)  # Canvas上中心点位置

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

    # 手动升温、降温  线程
    # 设置完后，t_use秒后动态显示设定的温度值
    def set_hands_temp(self, now_temp, target_temp, t_use):
        global connect, t_send_new, t_set  # 一般比下面的开始时间小，除非重新点击了设置按钮
        now_temp = int(now_temp)
        target_temp = int(target_temp)
        t_begin = time.time()
        temp = target_temp - now_temp  # 差值
        t_s = temp / t_use  # 每秒变化量
        for i in range(1, t_use + 1):
            if connect:  # 随时可跳出循环
                t_set = round((now_temp + i * t_s) + random.random(), 1)  # 生成随机（0， 1）
                time.sleep(1)
                if 1:
                    self.avg_num.set(t_set)  # 30路平均，值
                if t_send_new > t_begin:
                    break
            else:
                break
        while 1:  # 设置完后，动态显示
            random_t = random.randint(-2, 2) * random.random()  # 动态生成
            self.avg_num.set(round(t_set + random_t, 1))  # 30路平均，值
            time.sleep(1)
            if t_send_new > t_begin:
                break

    # 接收数据 主要函数
    # Z5A ('ok) X58 W57 V56    U55 T54 S53 R52 Q51   #标志的16进制
    def recvdata(self):
        global get_data_31, get_data_31_old, avg_num_sum
        print('开始接收数据。。。')
        get_data_31 = [-200] * 31  # 初始化，30路测量温度和1路环境温度
        if connect:
            print('had connect')
            try:
                self.recvbuf = str(self.sk.recv(t_len))  # 提取出接收到的数据
                readstr = eval(self.recvbuf.replace(' ', ''))  # 去掉空格,  从str转bytes
                print('num_接收', readstr, type(readstr), len(readstr))  # 得到接收的数据，及类型str，长度
                # b'S\x00\xe4\x00\xf1\x00\xdb', str, 7
                list_readstr = list(readstr)  # [87, 0, 215, 0, 221, 0, 225]
                self.write_re_log(list_readstr)  # 打印动态1，接收的数据   [87, 0, 215, 0, 221, 0, 225]

                for y in range(len(list_readstr) // 7):  # 把此次收到的数据都解析
                    list_y = list_readstr[7 * y:7 * y + 7]
                    list_3_shi = self.t6_get_3t(list_y)  # 输入[87, 0, 215, 0, 221, 0, 225]，输出（已除10）[21.5, 22.1, 22.5]
                    if list_3_shi:  # 有3个温度
                        if list_y[0] == 90:  # 匹配Z, 此路有平均温度
                            # agv0=round(reduce(lambda q, r: q + r, list_3_shi) / 3, 1)
                            # self.avg_num_0.set(agv0)  # Z，A三路均值
                            get_data_31[0:3] = list_3_shi
                            print('Z设置三路：', list_3_shi)
                        elif list_y[0] == 89:  # 匹配Y, 此路有平均温度
                            # self.avg_num_1.set(round(reduce(lambda q, r: q + r, list_3_shi) / 3, 1))  # Y，B三路均值
                            get_data_31[3:6] = list_3_shi
                            print('Y设置三路：', list_3_shi)
                        elif list_y[0] == 88:  # 匹配X, 此路有平均温度
                            # self.avg_num_2.set(round(reduce(lambda q, r: q + r, list_3_shi) / 3, 1))  # X，C三路均值
                            get_data_31[6:9] = list_3_shi
                            print('X设置三路：', list_3_shi)
                        elif list_y[0] == 87:  # 匹配W, 此路有平均温度
                            # self.avg_num_3.set(round(reduce(lambda q, r: q + r, list_3_shi) / 3, 1))  # W，D三路均值
                            get_data_31[9:12] = list_3_shi
                            print('W设置三路：', list_3_shi)
                        elif list_y[0] == 86:  # 匹配V, 此路有平均温度
                            # self.avg_num_4.set(round(reduce(lambda q, r: q + r, list_3_shi) / 3, 1))  # V，E三路均值
                            get_data_31[12:15] = list_3_shi
                            print('V设置三路：', list_3_shi)
                        elif list_y[0] == 85:  # 匹配U, 此路有平均温度
                            # self.avg_num_5.set(round(reduce(lambda q, r: q + r, list_3_shi) / 3, 1))  # U，F三路均值
                            get_data_31[15:18] = list_3_shi
                            print('U设置三路：', list_3_shi)
                        elif list_y[0] == 84:  # 匹配T, 此路有平均温度
                            # self.avg_num_6.set(round(reduce(lambda q, r: q + r, list_3_shi) / 3, 1))  # T，G三路均值
                            get_data_31[18:21] = list_3_shi
                            print('T设置三路：', list_3_shi)
                        elif list_y[0] == 83:  # 匹配S, 此路有平均温度
                            # self.avg_num_7.set(round(reduce(lambda q, r: q + r, list_3_shi) / 3, 1))  # S，H三路均值
                            get_data_31[21:24] = list_3_shi
                            print('S设置三路：', list_3_shi)
                        elif list_y[0] == 82:  # 匹配R, 此路有平均温度
                            # self.avg_num_8.set(round(reduce(lambda q, r: q + r, list_3_shi) / 3, 1))  # R，I三路均值
                            get_data_31[24:27] = list_3_shi
                            print('R设置三路：', list_3_shi)
                        elif list_y[0] == 81:  # 匹配Q, 此路有平均温度
                            # self.avg_num_9.set(round(reduce(lambda q, r: q + r, list_3_shi) / 3, 1))  # Q，J三路均值
                            get_data_31[27:30] = list_3_shi
                            print('Q设置三路：', list_3_shi)
                        elif list_y[0] == 121:  # 匹配y, 环境路有温度
                            # self.env_num.set(round(list_3_shi[0], 1))  # 环境，值
                            get_data_31[30] = list_3_shi[0]
                            print('y设置环境：', list_3_shi[0])
                        else:
                            print('没有匹配到A-J这10路和环境温度')
                    else:
                        print('没有3个数据')
                # 解析之后，把数据存到一个列表中[1*31]，传递给 son

                get_data_31_old = self.compare_200(get_data_31_old[0], get_data_31[:30])  # 返回2元元组，list+len
                avg_num_sum = round(
                    reduce(lambda q, r: q + r, self.trans_200(get_data_31_old[0])[:30]) / get_data_31_old[1],
                    1)  # 计算30路平均值
                # self.avg_num.set(avg_num_sum)  # 30路平均，值
                print('设置30路平均温度：', avg_num_sum)
                print('输出元组：', get_data_31_old)
                self.write_re_log(get_data_31_old)  # 打印动态2，返回给son的数组  ,([1*30],len)
            except Exception as e:
                print('err_接收', e)
        return get_data_31_old[0]  # 返回给类 SON 的温度数据 [1*31]，获取到的即为温度，否则值为-200

    def sendAllData(self, s):  # #
        global connect, hot_or_col, get_data_4hex_huan, t_send_new, t_set, avg_num_sum  # 00 24
        # avg_num_sum=1
        if connect:
            t_send_new = time.time()  # 每次点击  更新点击时间
            self.sendAllBuff = self.sendAllSet.get()  # 获取发送端口写下的数据  self.sendAllBuff==''
            if self.sendAllBuff == '':  # 为空
                if int(hot_or_col) == 1:
                    # s.send(bytes('#+', 'utf8'))  # 通过网口进行发送
                    # s.send(self.sendAllBuff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    # s.send(self.sendAllBuff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    # s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    # self.write_se_log('#+ ' + str(self.sendAllSet.get()))
                    s.send(bytes('#+' + 'NO num', 'utf8'))  # 通过网口进行发送 0D0A
                    self.write_se_log('#+' + 'NO num')
                else:
                    s.send(bytes('#-' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('#-' + 'NO num')
            else:  # 有数
                self.sendAllBuff = self.get_h_l(
                    self.int_transform_4hex(round(float(self.sendAllBuff), 1)))  # 23,ffce,(0, 230)
                if int(hot_or_col) == 1:
                    s.send(bytes('#+', 'utf8'))  # 通过网口进行发送
                    s.send(self.sendAllBuff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.sendAllBuff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('#+ ' + str(round(float(self.sendAllSet.get()), 1)))
                    if t_set == -100:  # 第一次
                        if avg_num_sum != -200:  # 有平均温度
                            self.set_hands_temp(avg_num_sum, self.sendAllSet.get(), 40)  # 升温50s
                    else:
                        self.set_hands_temp(t_set, self.sendAllSet.get(), 40)  # 升温50s
                else:
                    s.send(bytes('#-', 'utf8'))  # 通过网口进行发送
                    s.send(self.sendAllBuff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.sendAllBuff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('#- ' + str(round(float(self.sendAllSet.get()), 1)))
                    if t_set == -100:  # 第一次
                        if avg_num_sum != -200:  # 有平均温度
                            self.set_hands_temp(avg_num_sum, self.sendAllSet.get(), 50)  # 降温50s
                    else:
                        self.set_hands_temp(t_set, self.sendAllSet.get(), 50)  # 降温50s

            self.write_wendu_log('数据已发送')
        else:
            self.write_wendu_log('请连接后再发送')

    def send0Data(self, s):  # A
        global connect, hot_or_col, get_data_4hex_huan
        if connect:
            time.sleep(3)
            self.send0Buff = self.sendSet_0.get()  # 获取发送端口写下的数据  self.sendAllBuff==''
            if self.send0Buff == '':  # 为空
                if int(hot_or_col) == 1:
                    s.send(bytes('A+' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('A+' + 'NO num')
                else:
                    s.send(bytes('A-' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('A-' + 'NO num')
            else:
                self.send0Buff = self.get_h_l(self.int_transform_4hex(round(float(self.send0Buff), 1)))
                if int(hot_or_col) == 1:
                    s.send(bytes('A+', 'utf8'))  # 通过网口进行发送
                    s.send(self.send0Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send0Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('A+ ' + str(round(float(self.sendSet_0.get()), 1)) + '0D0A')
                else:
                    s.send(bytes('A-', 'utf8'))  # 通过网口进行发送
                    s.send(self.send0Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send0Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('A- ' + str(round(float(self.sendSet_0.get()), 1)) + '0D0A')
            self.write_wendu_log('数据已发送')
        else:
            self.write_wendu_log('请连接后再发送')

    def send1Data(self, s):  # B
        global connect, hot_or_col, get_data_4hex_huan
        if connect:
            self.send1Buff = self.sendSet_1.get()  # 获取发送端口写下的数据  self.sendAllBuff==''
            if self.send1Buff == '':  # 为空
                if int(hot_or_col) == 1:
                    s.send(bytes('B+' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('B+' + 'NO num')
                else:
                    s.send(bytes('B-' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('B-' + 'NO num')
            else:
                self.send1Buff = self.get_h_l(self.int_transform_4hex(round(float(self.send1Buff), 1)))
                if int(hot_or_col) == 1:
                    s.send(bytes('B+', 'utf8'))  # 通过网口进行发送
                    s.send(self.send1Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send1Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('B+ ' + str(round(float(self.sendSet_1.get()), 1)) + '0D0A')
                else:
                    s.send(bytes('B-', 'utf8'))  # 通过网口进行发送
                    s.send(self.send1Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send1Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('B- ' + str(round(float(self.sendSet_1.get()), 1)) + '0D0A')
            self.write_wendu_log('数据已发送')
        else:
            self.write_wendu_log('请连接后再发送')

    def send2Data(self, s):  # C
        global connect, hot_or_col, get_data_4hex_huan
        if connect:
            self.send2Buff = self.sendSet_2.get()  # 获取发送端口写下的数据  self.sendAllBuff==''
            if self.send2Buff == '':  # 为空
                if int(hot_or_col) == 1:
                    s.send(bytes('C+' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('C+' + 'NO num')
                else:
                    s.send(bytes('C-' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('C-' + 'NO num')
            else:
                self.send2Buff = self.get_h_l(self.int_transform_4hex(round(float(self.send2Buff), 1)))
                if int(hot_or_col) == 1:
                    s.send(bytes('C+', 'utf8'))  # 通过网口进行发送
                    s.send(self.send2Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send2Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('C+' + str(round(float(self.sendSet_2.get()), 1)) + '0D0A')
                else:
                    s.send(bytes('C- ', 'utf8'))  # 通过网口进行发送
                    s.send(self.send2Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send2Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('C- ' + str(round(float(self.sendSet_2.get()), 1)) + '0D0A')
            self.write_wendu_log('数据已发送')
        else:
            self.write_wendu_log('请连接后再发送')

    def send3Data(self, s):  # D
        global connect, hot_or_col, get_data_4hex_huan
        if connect:
            self.send3Buff = self.sendSet_3.get()  # 获取发送端口写下的数据  self.sendAllBuff==''
            if self.send3Buff == '':  # 为空
                if int(hot_or_col) == 1:
                    s.send(bytes('D+' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('D+' + 'NO num')
                else:
                    s.send(bytes('D-' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('D-' + 'NO num')
            else:
                self.send3Buff = self.get_h_l(self.int_transform_4hex(round(float(self.send3Buff), 1)))
                if int(hot_or_col) == 1:
                    s.send(bytes('D+', 'utf8'))  # 通过网口进行发送
                    s.send(self.send3Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send3Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('D+ ' + str(round(float(self.sendSet_3.get()), 1)) + '0D0A')
                else:
                    s.send(bytes('D-', 'utf8'))  # 通过网口进行发送
                    s.send(self.send3Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send3Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('D- ' + str(round(float(self.sendSet_3.get()), 1)) + '0D0A')
            self.write_wendu_log('数据已发送')
        else:
            self.write_wendu_log('请连接后再发送')

    def send4Data(self, s):  # E
        global connect, hot_or_col, get_data_4hex_huan
        if connect:
            self.send4Buff = self.sendSet_4.get()  # 获取发送端口写下的数据  self.sendAllBuff==''
            if self.send4Buff == '':  # 为空
                if int(hot_or_col) == 1:
                    s.send(bytes('E+' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('E+' + 'NO num')
                else:
                    s.send(bytes('E-' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('E-' + 'NO num')
            else:
                self.send4Buff = self.get_h_l(self.int_transform_4hex(round(float(self.send4Buff), 1)))
                if int(hot_or_col) == 1:
                    s.send(bytes('E+', 'utf8'))  # 通过网口进行发送
                    s.send(self.send4Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send4Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('E+ ' + str(round(float(self.sendSet_4.get()), 1)) + '0D0A')
                else:
                    s.send(bytes('E-', 'utf8'))  # 通过网口进行发送
                    s.send(self.send4Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send4Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('E- ' + str(round(float(self.sendSet_4.get()), 1)) + '0D0A')
            self.write_wendu_log('数据已发送')
        else:
            self.write_wendu_log('请连接后再发送')

    def send5Data(self, s):  # F
        global connect, hot_or_col, get_data_4hex_huan
        if connect:
            self.send5Buff = self.sendSet_5.get()  # 获取发送端口写下的数据  self.sendAllBuff==''
            if self.send5Buff == '':  # 为空
                if int(hot_or_col) == 1:
                    s.send(bytes('F+' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('F+' + 'NO num')
                else:
                    s.send(bytes('F-' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('F-' + 'NO num')
            else:
                self.send5Buff = self.get_h_l(self.int_transform_4hex(round(float(self.send5Buff), 1)))
                if int(hot_or_col) == 1:
                    s.send(bytes('F+', 'utf8'))  # 通过网口进行发送
                    s.send(self.send5Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send5Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('F+ ' + str(round(float(self.sendSet_5.get()), 1)) + '0D0A')
                else:
                    s.send(bytes('F-', 'utf8'))  # 通过网口进行发送
                    s.send(self.send5Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send5Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('F- ' + str(round(float(self.sendSet_5.get()), 1)) + '0D0A')
            self.write_wendu_log('数据已发送')
        else:
            self.write_wendu_log('请连接后再发送')

    def send6Data(self, s):  # G
        global connect, hot_or_col, get_data_4hex_huan
        if connect:
            self.send6Buff = self.sendSet_6.get()  # 获取发送端口写下的数据  self.sendAllBuff==''
            if self.send6Buff == '':  # 为空
                if int(hot_or_col) == 1:
                    s.send(bytes('G+' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('G+' + 'NO num')
                else:
                    s.send(bytes('G-' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('G-' + 'NO num')
            else:
                self.send6Buff = self.get_h_l(self.int_transform_4hex(round(float(self.send6Buff), 1)))
                if int(hot_or_col) == 1:
                    s.send(bytes('G+', 'utf8'))  # 通过网口进行发送
                    s.send(self.send6Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send6Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('G+ ' + str(round(float(self.sendSet_6.get()), 1)) + '0D0A')
                else:
                    s.send(bytes('G-', 'utf8'))  # 通过网口进行发送
                    s.send(self.send6Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send6Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('G- ' + str(round(float(self.sendSet_6.get()), 1)) + '0D0A')
            self.write_wendu_log('数据已发送')
        else:
            self.write_wendu_log('请连接后再发送')

    def send7Data(self, s):  # H
        global connect, hot_or_col, get_data_4hex_huan
        if connect:
            self.send7Buff = self.sendSet_7.get()  # 获取发送端口写下的数据  self.sendAllBuff==''
            if self.send7Buff == '':  # 为空
                if int(hot_or_col) == 1:
                    s.send(bytes('H+' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('H+' + 'NO num')
                else:
                    s.send(bytes('H-' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('H-' + 'NO num')
            else:
                self.send7Buff = self.get_h_l(self.int_transform_4hex(round(float(self.send7Buff), 1)))
                if int(hot_or_col) == 1:
                    s.send(bytes('H+', 'utf8'))  # 通过网口进行发送
                    s.send(self.send7Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send7Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('H+ ' + str(round(float(self.sendSet_7.get()), 1)) + '0D0A')
                else:
                    s.send(bytes('H-', 'utf8'))  # 通过网口进行发送
                    s.send(self.send7Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send7Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('H- ' + str(round(float(self.sendSet_7.get()), 1)) + '0D0A')
            self.write_wendu_log('数据已发送')
        else:
            self.write_wendu_log('请连接后再发送')

    def send8Data(self, s):  # I
        global connect, hot_or_col, get_data_4hex_huan
        if connect:
            self.send8Buff = self.sendSet_8.get()  # 获取发送端口写下的数据  self.sendAllBuff==''
            if self.send8Buff == '':  # 为空
                if int(hot_or_col) == 1:
                    s.send(bytes('I+' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('I+' + 'NO num')
                else:
                    s.send(bytes('I-' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('I-' + 'NO num')
            else:
                self.send8Buff = self.get_h_l(self.int_transform_4hex(round(float(self.send8Buff), 1)))
                if int(hot_or_col) == 1:
                    s.send(bytes('I+', 'utf8'))  # 通过网口进行发送
                    s.send(self.send8Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send8Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('I+ ' + str(round(float(self.sendSet_8.get()), 1)) + '0D0A')
                else:
                    s.send(bytes('I-', 'utf8'))  # 通过网口进行发送
                    s.send(self.send8Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send8Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('I- ' + str(round(float(self.sendSet_8.get()), 1)) + '0D0A')
            self.write_wendu_log('数据已发送')
        else:
            self.write_wendu_log('请连接后再发送')

    def send9Data(self, s):  # J
        global connect, hot_or_col, get_data_4hex_huan
        if connect:
            self.send9Buff = self.sendSet_9.get()  # 获取发送端口写下的数据  self.sendAllBuff==''
            if self.send9Buff == '':  # 为空
                if int(hot_or_col) == 1:
                    s.send(bytes('J+' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('J+' + 'NO num')
                else:
                    s.send(bytes('J-' + 'NO num', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('J-' + 'NO num')
            else:
                self.send9Buff = self.get_h_l(
                    self.int_transform_4hex(round(float(self.send9Buff), 1)))  # ff ce, (255 206)
                if int(hot_or_col) == 1:
                    s.send(bytes('J+', 'utf8'))  # 通过网口进行发送
                    s.send(self.send9Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send9Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('J+ ' + str(round(float(self.sendSet_9.get()), 1)) + '0D0A')
                else:
                    s.send(bytes('J-', 'utf8'))  # 通过网口进行发送
                    s.send(self.send9Buff[0].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(self.send9Buff[1].to_bytes(1, byteorder='big'))  # 通过网口进行发送
                    s.send(bytes('\r\n', 'utf8'))  # 通过网口进行发送
                    self.write_se_log('J- ' + str(round(float(self.sendSet_9.get()), 1)) + '0D0A')
            self.write_wendu_log('数据已发送')
        else:
            self.write_wendu_log('请连接后再发送')

    # 纯按钮功能
    def sendTData(self, s, arges):
        global connect
        if connect:
            try:
                self.sendBuff = arges
                print('1111111')
                s.send(bytes(self.sendBuff + '\r\n', 'utf8'))  # 通过网口进行发送
                # arges=self.get_h_l(arges)
                # aa=arges[0].to_bytes(1,byteorder='big')
                # ab=arges[1].to_bytes(1,byteorder='big')
                # print(aa,ab)
                # s.send(aa)  # 通过网口进行发送 16 进制
                # s.send(ab)  # 通过网口进行发送
                # # s.send('#-', self.sendBuff)  # 通过网口进行发送
                self.write_se_log(self.sendBuff)
                self.write_wendu_log('数据已发送')
            except:
                print('-1')
        else:
            self.write_wendu_log('请连接后再发送')
        return

    # 对senddata()和recvdata()方法采用多线程
    def sending(self, s):
        t = threading.Thread(target=self.senddata, args=(s,))
        t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        t.start()  # 开启线程
        return

    def sendAlling(self, s):
        t = threading.Thread(target=self.sendAllData, args=(s,))
        t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        t.start()  # 开启线程
        return

    def send0ing(self, s):
        t = threading.Thread(target=self.send0Data, args=(s,))
        t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        t.start()  # 开启线程
        return

    def send1ing(self, s):
        t = threading.Thread(target=self.send1Data, args=(s,))
        t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        t.start()  # 开启线程
        return

    def send2ing(self, s):
        t = threading.Thread(target=self.send2Data, args=(s,))
        t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        t.start()  # 开启线程
        return

    def send3ing(self, s):
        t = threading.Thread(target=self.send3Data, args=(s,))
        t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        t.start()  # 开启线程
        return

    def send4ing(self, s):
        t = threading.Thread(target=self.send4Data, args=(s,))
        t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        t.start()  # 开启线程
        return

    def send5ing(self, s):
        t = threading.Thread(target=self.send5Data, args=(s,))
        t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        t.start()  # 开启线程
        return

    def send6ing(self, s):
        t = threading.Thread(target=self.send6Data, args=(s,))
        t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        t.start()  # 开启线程
        return

    def send7ing(self, s):
        t = threading.Thread(target=self.send7Data, args=(s,))
        t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        t.start()  # 开启线程
        return

    def send8ing(self, s):
        t = threading.Thread(target=self.send8Data, args=(s,))
        t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        t.start()  # 开启线程
        return

    def send9ing(self, s):
        t = threading.Thread(target=self.send9Data, args=(s,))
        t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        t.start()  # 开启线程
        return

    def sendTing(self, s, arges):  # 通用发送函数
        t = threading.Thread(target=self.sendTData, args=(s, arges,))
        t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程
        t.start()  # 开启线程
        return

    def recving(self):
        global connect, hot_or_col
        print('connect', connect, hot_or_col)
        if connect:
            t = threading.Thread(target=self.recvdata)
            t.setDaemon(True)  # 设置为后台线程，这里默认是False，设置为True之后则主线程不用等待子线程 self.sk
            t.start()  # 开启线程
            # print('dakai threading', t.name)

    # 十进制（正负一位小数） 转4位16进制  输入24 输出 00f0
    def int_transform_4hex(self, intNums):
        try:
            intNums = str(intNums).replace(' ', '')
            intNums = int(float(intNums) * 10)  # 已乘以10
            if intNums < 0:  # 如果是负数
                str_list_16nums = list(hex(intNums % 65536))
                insert_num = 'f'
            else:  # 如果是正数
                str_list_16nums = list(hex(intNums))
                insert_num = '0'
            # 补位数
            if len(str_list_16nums) == 5:
                str_list_16nums.insert(2, insert_num)
            elif len(str_list_16nums) == 4:
                str_list_16nums.insert(2, insert_num)
                str_list_16nums.insert(2, insert_num)
            elif len(str_list_16nums) == 3:
                str_list_16nums.insert(2, insert_num)
                str_list_16nums.insert(2, insert_num)
                str_list_16nums.insert(2, insert_num)
            else:
                pass
            crc_data = "".join(str_list_16nums)  # 用""把数组的每一位结合起来  组成新的字符串
            hexNums = crc_data[2:4] + ' ' + crc_data[4:]
        except:
            print('err_int_transform_4hex')
        return hexNums

    # 输入两个列表,长度30，输出新的列表和非-200的个数(元组的形式)
    def compare_200(self, list_old, list_new):
        len_new = len(list_new)
        num_other = 0
        if len_new == 30:
            for i in range(30):
                if list_new[i] != -200:
                    list_old[i] = list_new[i]  # 更新新的温度数值
        for j in range(30):
            if list_old[j] != -200:
                num_other += 1
        return list_old, num_other

    # 输入列表，元素为-200即变0，返回处理后的列表
    def trans_200(self, arges_list):
        for i in range(len(arges_list)):
            if arges_list[i] == -200:
                arges_list[i] = 0
        return arges_list

    # 输入ff ce  输出 255 206
    def get_h_l(self, arges):
        arges = str(arges).replace(' ', '')
        int_a = int(arges, 16)
        hight_8 = int_a & 0x00ff
        lower_8 = int_a >> 8
        return lower_8, hight_8

    # 4位16进制转十进制（正负）  输入 00ff 输出 24
    def hex4_transform_int(self, hex_num):  # 输入 ff9c  ff 9c
        try:
            hex_num = hex_num.replace(' ', '')  # 去掉空格
            we = '-1 & 0x' + hex_num  # 结合
            b_2 = ''
            add_f = 0  # 负数之和
            b = bin(eval(we))  # 清除格式
            if len(b) <= 14:  # 正数，3位   太大
                get_num = self.hex4_transform_intz(hex_num)
            elif len(b) == 18:  # 负数
                b_2 = [int(_) for _ in b[2:]]  # 取后面16位
                for i in range(1, len(b_2)):
                    if b_2[i]:
                        b_2[i] = 0
                    else:
                        b_2[i] = 1
                b_2[0] = 1
                b_2 = b_2[1:][::-1]
                for x in range(len(b_2)):
                    add_f += b_2[x] * 2 ** x
                get_num = -add_f - 1
            else:
                return -1
        except:
            print('err_hex4_transform_int')
        return get_num

    def hex2dec(self, string_num):
        return str(int(string_num.upper(), 16))

    def hex4_transform_intz(self, hex_num):
        num = 0
        hex_num = hex_num[::-1]
        for i in range(len(hex_num)):
            j = int(self.hex2dec(hex_num[i]))
            num += j * 16 ** i
        return num

    # 输入[87, 0, 215, 0, 221, 0, 225]，输出[21.5, 22.1, 22.5]（已除以10）,用其他函数
    def t6_get_3t(self, arges):
        ans = []
        if len(arges) == 7:
            hex_6 = list(map(lambda x: hex(x)[2:].zfill(2), arges[1:]))  # 6个10进制转6个16进制
            for i in range(3):
                hex_2 = hex_6[2 * i] + hex_6[2 * i + 1]  # 两两16进制组合
                int_2 = self.hex4_transform_int(hex_2)  # 1组合16进制转10进制温度（正负）
                ans.append(int_2 / 10)  # 存到列表中
        return ans

    # 更新缓存区
    def update(self):
        global num_updata_in, connect, t1
        if connect:
            if t1 == 1:
                pass
                self.sendTData(self.sk, 'BR')  # 默认发指令  '#R'
            elif t1 >= 200:  # 200*0.5s的周期
                t1 = 0
            t1 += 1
        try:
            self.recving()  # 接收数据
        except Exception as e:
            print(e)
        self.init_window_name.after(num_updata_in, self.update)

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

    # 平均温度和环境温度框
    def all_env(self):
        self.f_avg = tkFont.Font(family='microsoft yahei', size=16, weight='bold')
        self.avg_label = Label(self.init_window_name, text="平均温度", bg="#F0FFFF", font=("仿宋", 20))  # 平均温度标签
        self.avg_label.place(relx=x1[1], rely=y1[0], anchor=CENTER)
        self.env_label = Label(self.init_window_name, text="环境温度", bg="#F0FFFF", font=("仿宋", 20))  # 环境温度标签
        self.env_label.place(relx=x1[3], rely=y1[0], anchor=CENTER)
        self.avg = Label(self.init_window_name, textvariable=self.avg_num, width=6, height=2, font=("仿宋", 40),
                         bg='#FFFAFA', relief='groove', bd=5)  # 平均温度框 不能改变
        self.avg.place(relx=x1[1], rely=y1[2], anchor=CENTER)
        self.env = Label(self.init_window_name, textvariable=self.env_num, width=6, height=2, font=("仿宋", 40),
                         bg='#FFFAFA', relief='groove', bd=5)  # 环境温度框 不能改变
        self.env.place(relx=x1[3], rely=y1[2], anchor=CENTER)

        # self.avg_num.set('ok')  # 平均温度设置
        # self.env_num.set('ok')  # 环境温度设置

    # 整体温度设置框
    def all_set(self):
        self.maxhot_text = """
最大制热
功率
        """
        self.maxcold_text = """
最大制冷
功率
        """
        self.tSet_text = """
关闭
通道
        """
        self.allSet_text = """
设置
温度
        """
        self.all_label = Label(self.init_window_name, text="整体温度设置", bg="#F0FFFF", font=("仿宋", 20))  # 平均温度标签
        self.all_label.place(relx=x1[6], rely=y1[0], anchor=CENTER)
        self.btn_MaxHot = Button(self.init_window_name, text=self.maxhot_text,
                                 command=lambda: self.sendTData(self.sk, '#H'),
                                 bg="#FF8C00", width=10, height=2, cursor='hand2', font=("仿宋", 15))  # 发送固定的指令#H
        self.btn_MaxHot.place(relx=x1[5], rely=y1[2] - 0.05, anchor=CENTER)
        self.btn_MaxCold = Button(self.init_window_name, text=self.maxcold_text,
                                  command=lambda: self.sendTData(self.sk, '#C'),
                                  bg="#FF8C00", width=10, height=2, cursor='hand2', font=("仿宋", 15))  # 发送固定的指令#C
        self.btn_MaxCold.place(relx=x1[5], rely=y1[2] + 0.05, anchor=CENTER)

        self.allSet = Entry(self.init_window_name, textvariable=self.sendAllSet, width=5, font=("仿宋", 31))  # 整体数据录入框
        self.allSet.place(relx=x1[8] - 0.04, rely=y1[2] - 0.05, anchor=CENTER)
        self.btn_allSet = Button(self.init_window_name, text=self.allSet_text, command=lambda: self.sendAlling(self.sk),
                                 bg="#FF8C00", width=10, height=2, cursor='hand2', font=("仿宋", 15))
        self.btn_allSet.place(relx=x1[8] - 0.04, rely=y1[2] + 0.05, anchor=CENTER)
        self.btn_tSet = Button(self.init_window_name, text=self.tSet_text,
                               command=lambda: self.sendTData(self.sk, '#T'),
                               bg="#FF8C00", width=10, height=2, cursor='hand2', font=("仿宋", 15))  # 发送固定的指令#T
        self.btn_tSet.place(relx=x1[6] + 0.03, rely=y1[2], anchor=CENTER)

    # 10路平均温度框
    def ten_avg(self):
        self.tenAvg_label = Label(self.init_window_name, text="平均温度显示", bg="#F0FFFF", font=("楷", 12))  # 平均温度标签
        self.tenAvg_label.place(relx=x1[0], rely=y1[5], anchor=CENTER)
        self.avg_0 = Label(self.init_window_name, textvariable=self.avg_num_0, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_0.place(relx=x1[0], rely=y1[6], anchor=CENTER)
        self.avg_1 = Label(self.init_window_name, textvariable=self.avg_num_1, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_1.place(relx=x1[1], rely=y1[6], anchor=CENTER)
        self.avg_2 = Label(self.init_window_name, textvariable=self.avg_num_2, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_2.place(relx=x1[2], rely=y1[6], anchor=CENTER)
        self.avg_3 = Label(self.init_window_name, textvariable=self.avg_num_3, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_3.place(relx=x1[3], rely=y1[6], anchor=CENTER)
        self.avg_4 = Label(self.init_window_name, textvariable=self.avg_num_4, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_4.place(relx=x1[4], rely=y1[6], anchor=CENTER)
        self.avg_5 = Label(self.init_window_name, textvariable=self.avg_num_5, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_5.place(relx=x1[5], rely=y1[6], anchor=CENTER)
        self.avg_6 = Label(self.init_window_name, textvariable=self.avg_num_6, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_6.place(relx=x1[6], rely=y1[6], anchor=CENTER)
        self.avg_7 = Label(self.init_window_name, textvariable=self.avg_num_7, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_7.place(relx=x1[7], rely=y1[6], anchor=CENTER)
        self.avg_8 = Label(self.init_window_name, textvariable=self.avg_num_8, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_8.place(relx=x1[8], rely=y1[6], anchor=CENTER)
        self.avg_9 = Label(self.init_window_name, textvariable=self.avg_num_9, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_9.place(relx=x1[9], rely=y1[6], anchor=CENTER)

        self.avg_num_0.set('ok')
        self.avg_num_1.set('ok')
        self.avg_num_2.set('ok')
        self.avg_num_3.set('ok')
        self.avg_num_4.set('ok')
        self.avg_num_5.set('ok')
        self.avg_num_6.set('ok')
        self.avg_num_7.set('ok')
        self.avg_num_8.set('ok')
        self.avg_num_9.set('ok')

    # 10路温度设置框
    def ten_set(self):
        self.tenSet_label = Label(self.init_window_name, text="局部温度设置", bg="#F0FFFF", font=("楷", 12))  # 平均温度标签
        self.tenSet_label.place(relx=x2[0], rely=y2[0], anchor=CENTER)
        self.set_0 = Entry(self.init_window_name, textvariable=self.sendSet_0, width=w1,
                           font=(ziti, zihao))  # 0路数据录入框 init_data_Text
        self.set_0.place(relx=x1[0], rely=y2[1], anchor=CENTER)
        self.set_1 = Entry(self.init_window_name, textvariable=self.sendSet_1, width=w1,
                           font=(ziti, zihao))  # 1路数据录入框 init_data_Text
        self.set_1.place(relx=x1[1], rely=y2[1], anchor=CENTER)
        self.set_2 = Entry(self.init_window_name, textvariable=self.sendSet_2, width=w1,
                           font=(ziti, zihao))  # 2路数据录入框 init_data_Text
        self.set_2.place(relx=x1[2], rely=y2[1], anchor=CENTER)
        self.set_3 = Entry(self.init_window_name, textvariable=self.sendSet_3, width=w1,
                           font=(ziti, zihao))  # 3路数据录入框 init_data_Text
        self.set_3.place(relx=x1[3], rely=y2[1], anchor=CENTER)
        self.set_4 = Entry(self.init_window_name, textvariable=self.sendSet_4, width=w1,
                           font=(ziti, zihao))  # 4路数据录入框 init_data_Text
        self.set_4.place(relx=x1[4], rely=y2[1], anchor=CENTER)
        self.set_5 = Entry(self.init_window_name, textvariable=self.sendSet_5, width=w1,
                           font=(ziti, zihao))  # 5路数据录入框 init_data_Text
        self.set_5.place(relx=x1[5], rely=y2[1], anchor=CENTER)
        self.set_6 = Entry(self.init_window_name, textvariable=self.sendSet_6, width=w1,
                           font=(ziti, zihao))  # 6路数据录入框 init_data_Text
        self.set_6.place(relx=x1[6], rely=y2[1], anchor=CENTER)
        self.set_7 = Entry(self.init_window_name, textvariable=self.sendSet_7, width=w1,
                           font=(ziti, zihao))  # 7路数据录入框 init_data_Text
        self.set_7.place(relx=x1[7], rely=y2[1], anchor=CENTER)
        self.set_8 = Entry(self.init_window_name, textvariable=self.sendSet_8, width=w1,
                           font=(ziti, zihao))  # 8路数据录入框 init_data_Text
        self.set_8.place(relx=x1[8], rely=y2[1], anchor=CENTER)
        self.set_9 = Entry(self.init_window_name, textvariable=self.sendSet_9, width=w1,
                           font=(ziti, zihao))  # 9路数据录入框 init_data_Text
        self.set_9.place(relx=x1[9], rely=y2[1], anchor=CENTER)

        self.btn_set_0 = Button(self.init_window_name, text='按钮0', command=lambda: self.send0ing(self.sk), bg="#FF8C00",
                                cursor='hand2', font=(ziti, zihao))  # 发送此路的温度数据
        self.btn_set_0.place(relx=x1[0], rely=y2[2], anchor=CENTER)
        self.btn_set_1 = Button(self.init_window_name, text='按钮1', command=lambda: self.send1ing(self.sk), bg="#FF8C00",
                                cursor='hand2', font=(ziti, zihao))
        self.btn_set_1.place(relx=x1[1], rely=y2[2], anchor=CENTER)
        self.btn_set_2 = Button(self.init_window_name, text='按钮2', command=lambda: self.send2ing(self.sk), bg="#FF8C00",
                                cursor='hand2', font=(ziti, zihao))
        self.btn_set_2.place(relx=x1[2], rely=y2[2], anchor=CENTER)
        self.btn_set_3 = Button(self.init_window_name, text='按钮3', command=lambda: self.send3ing(self.sk), bg="#FF8C00",
                                cursor='hand2', font=(ziti, zihao))
        self.btn_set_3.place(relx=x1[3], rely=y2[2], anchor=CENTER)
        self.btn_set_4 = Button(self.init_window_name, text='按钮4', command=lambda: self.send4ing(self.sk), bg="#FF8C00",
                                cursor='hand2', font=(ziti, zihao))
        self.btn_set_4.place(relx=x1[4], rely=y2[2], anchor=CENTER)
        self.btn_set_5 = Button(self.init_window_name, text='按钮5', command=lambda: self.send5ing(self.sk), bg="#FF8C00",
                                cursor='hand2', font=(ziti, zihao))
        self.btn_set_5.place(relx=x1[5], rely=y2[2], anchor=CENTER)
        self.btn_set_6 = Button(self.init_window_name, text='按钮6', command=lambda: self.send6ing(self.sk), bg="#FF8C00",
                                cursor='hand2', font=(ziti, zihao))
        self.btn_set_6.place(relx=x1[6], rely=y2[2], anchor=CENTER)
        self.btn_set_7 = Button(self.init_window_name, text='按钮7', command=lambda: self.send7ing(self.sk), bg="#FF8C00",
                                cursor='hand2', font=(ziti, zihao))
        self.btn_set_7.place(relx=x1[7], rely=y2[2], anchor=CENTER)
        self.btn_set_8 = Button(self.init_window_name, text='按钮8', command=lambda: self.send8ing(self.sk), bg="#FF8C00",
                                cursor='hand2', font=(ziti, zihao))
        self.btn_set_8.place(relx=x1[8], rely=y2[2], anchor=CENTER)
        self.btn_set_9 = Button(self.init_window_name, text='按钮9', command=lambda: self.send9ing(self.sk), bg="#FF8C00",
                                cursor='hand2', font=(ziti, zihao))
        self.btn_set_9.place(relx=x1[9], rely=y2[2], anchor=CENTER)

        self.btn_set_at = Button(self.init_window_name, text='关闭0', command=lambda: self.sendTData(self.sk, 'AT'),
                                 bg="#FF8C00", cursor='hand2', font=(ziti, zihao))  # 发送固定的指令AT
        self.btn_set_at.place(relx=x1[0], rely=y2[3], anchor=CENTER)
        self.btn_set_bt = Button(self.init_window_name, text='关闭1', command=lambda: self.sendTData(self.sk, 'BT'),
                                 bg="#FF8C00", cursor='hand2', font=(ziti, zihao))
        self.btn_set_bt.place(relx=x1[1], rely=y2[3], anchor=CENTER)
        self.btn_set_ct = Button(self.init_window_name, text='关闭2', command=lambda: self.sendTData(self.sk, 'CT'),
                                 bg="#FF8C00", cursor='hand2', font=(ziti, zihao))
        self.btn_set_ct.place(relx=x1[2], rely=y2[3], anchor=CENTER)
        self.btn_set_dt = Button(self.init_window_name, text='关闭3', command=lambda: self.sendTData(self.sk, 'DT'),
                                 bg="#FF8C00", cursor='hand2', font=(ziti, zihao))
        self.btn_set_dt.place(relx=x1[3], rely=y2[3], anchor=CENTER)
        self.btn_set_et = Button(self.init_window_name, text='关闭4', command=lambda: self.sendTData(self.sk, 'ET'),
                                 bg="#FF8C00", cursor='hand2', font=(ziti, zihao))
        self.btn_set_et.place(relx=x1[4], rely=y2[3], anchor=CENTER)
        self.btn_set_ft = Button(self.init_window_name, text='关闭5', command=lambda: self.sendTData(self.sk, 'FT'),
                                 bg="#FF8C00", cursor='hand2', font=(ziti, zihao))
        self.btn_set_ft.place(relx=x1[5], rely=y2[3], anchor=CENTER)
        self.btn_set_gt = Button(self.init_window_name, text='关闭6', command=lambda: self.sendTData(self.sk, 'GT'),
                                 bg="#FF8C00", cursor='hand2', font=(ziti, zihao))
        self.btn_set_gt.place(relx=x1[6], rely=y2[3], anchor=CENTER)
        self.btn_set_ht = Button(self.init_window_name, text='关闭7', command=lambda: self.sendTData(self.sk, 'HT'),
                                 bg="#FF8C00", cursor='hand2', font=(ziti, zihao))
        self.btn_set_ht.place(relx=x1[7], rely=y2[3], anchor=CENTER)
        self.btn_set_it = Button(self.init_window_name, text='关闭8', command=lambda: self.sendTData(self.sk, 'IT'),
                                 bg="#FF8C00", cursor='hand2', font=(ziti, zihao))
        self.btn_set_it.place(relx=x1[8], rely=y2[3], anchor=CENTER)
        self.btn_set_jt = Button(self.init_window_name, text='关闭9', command=lambda: self.sendTData(self.sk, 'JT'),
                                 bg="#FF8C00", cursor='hand2', font=(ziti, zihao))
        self.btn_set_jt.place(relx=x1[9], rely=y2[3], anchor=CENTER)


class SON(FATHER):
    def __init__(self, window_name):
        self.window_name = window_name

    def set_son_window(self, root):
        self.menubar = Menu(root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="30路温度", command=self.about)
        self.menubar.add_cascade(label="查看", menu=self.filemenu)
        root.config(menu=self.menubar)

    def about(self):  # about子窗口定义
        global num_updata_out, connect

        self.in_data_num_00 = StringVar()  #
        self.in_data_num_01 = StringVar()
        self.in_data_num_02 = StringVar()
        self.in_data_num_03 = StringVar()
        self.in_data_num_04 = StringVar()  #
        self.in_data_num_05 = StringVar()
        self.in_data_num_06 = StringVar()
        self.in_data_num_07 = StringVar()
        self.in_data_num_08 = StringVar()  #
        self.in_data_num_09 = StringVar()

        self.in_data_num_10 = StringVar()  #
        self.in_data_num_11 = StringVar()
        self.in_data_num_12 = StringVar()
        self.in_data_num_13 = StringVar()
        self.in_data_num_14 = StringVar()  #
        self.in_data_num_15 = StringVar()
        self.in_data_num_16 = StringVar()
        self.in_data_num_17 = StringVar()
        self.in_data_num_18 = StringVar()  #
        self.in_data_num_19 = StringVar()

        self.in_data_num_20 = StringVar()  #
        self.in_data_num_21 = StringVar()
        self.in_data_num_22 = StringVar()
        self.in_data_num_23 = StringVar()
        self.in_data_num_24 = StringVar()  #
        self.in_data_num_25 = StringVar()
        self.in_data_num_26 = StringVar()
        self.in_data_num_27 = StringVar()
        self.in_data_num_28 = StringVar()  #
        self.in_data_num_29 = StringVar()

        # self.in_data_num_30=StringVar()   #
        # self.in_data_num_31=StringVar()
        # self.in_data_num_32=StringVar()
        # self.in_data_num_33=StringVar()
        # self.in_data_num_34=StringVar()   #
        # self.in_data_num_35=StringVar()
        # self.in_data_num_36=StringVar()
        # self.in_data_num_37=StringVar()
        # self.in_data_num_38=StringVar()   #
        # self.in_data_num_39=StringVar()

        # self.in_data_num_40=StringVar()   #
        # self.in_data_num_41=StringVar()
        # self.in_data_num_42=StringVar()
        # self.in_data_num_43=StringVar()
        # self.in_data_num_44=StringVar()   #
        # self.in_data_num_45=StringVar()
        # self.in_data_num_46=StringVar()
        # self.in_data_num_47=StringVar()
        # self.in_data_num_48=StringVar()   #
        # self.in_data_num_49=StringVar()

        self.avg_num_0 = StringVar()  #
        self.avg_num_1 = StringVar()
        self.avg_num_2 = StringVar()
        self.avg_num_3 = StringVar()
        self.avg_num_4 = StringVar()
        self.avg_num_5 = StringVar()
        self.avg_num_6 = StringVar()
        self.avg_num_7 = StringVar()
        self.avg_num_8 = StringVar()
        self.avg_num_9 = StringVar()

        self.top = Toplevel()
        self.top.geometry("1068x481+10+10")  # 子窗口大小
        self.top.title("30路温度具体数据")
        # self.recorde_label = Label(self.top, text='接收的', bg="#ffffff")
        # self.recorde_label.place(relx=x3[6], rely=y_text - 0.4, anchor=CENTER)
        # self.recorde = scrolledtext.ScrolledText(self.top, width=40, height=6)
        # self.recorde.place(relx=x3[7], rely=y_show - 0.3, anchor=CENTER)
        self.in_data()  # 显示上面5*10个框
        self.ten_avg()

        self.window_name.after(num_updata_out, self.update)

    # 接收数据 并展现在son中
    def set_30_data(self, arges):  # 输入1*31路，默认-200,其他为温度数值
        global hot_or_col, h1, cc, t_len, hex_cc, tem_min, tem_max
        try:
            if arges[0] != -200:
                self.in_data_num_00.set(round(arges[0], 1))  # 下面10路平均温度设置，保留1位小数
                self.avg_num_0.set(round((arges[0] + arges[1] + arges[2]) / 3, 1))
            if arges[1] != -200:
                self.in_data_num_10.set(round(arges[1], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[2] != -200:
                self.in_data_num_20.set(round(arges[2], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[3] != -200:
                self.in_data_num_01.set(round(arges[3], 1))  # 下面10路平均温度设置，保留1位小数
                self.avg_num_1.set(round((arges[3] + arges[4] + arges[5]) / 3, 1))
            if arges[4] != -200:
                self.in_data_num_11.set(round(arges[4], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[5] != -200:
                self.in_data_num_21.set(round(arges[5], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[6] != -200:
                self.in_data_num_02.set(round(arges[6], 1))  # 下面10路平均温度设置，保留1位小数
                self.avg_num_2.set(round((arges[6] + arges[7] + arges[8]) / 3, 1))
            if arges[7] != -200:
                self.in_data_num_12.set(round(arges[7], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[8] != -200:
                self.in_data_num_22.set(round(arges[8], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[9] != -200:
                self.in_data_num_03.set(round(arges[9], 1))  # 下面10路平均温度设置，保留1位小数
                self.avg_num_3.set(round((arges[9] + arges[10] + arges[11]) / 3, 1))
            if arges[10] != -200:
                self.in_data_num_13.set(round(arges[10], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[11] != -200:
                self.in_data_num_23.set(round(arges[11], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[12] != -200:
                self.in_data_num_04.set(round(arges[12], 1))  # 下面10路平均温度设置，保留1位小数
                self.avg_num_4.set(round((arges[12] + arges[13] + arges[14]) / 3, 1))
            if arges[13] != -200:
                self.in_data_num_14.set(round(arges[13], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[14] != -200:
                self.in_data_num_24.set(round(arges[14], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[15] != -200:
                self.in_data_num_05.set(round(arges[15], 1))  # 下面10路平均温度设置，保留1位小数
                self.avg_num_5.set(round((arges[15] + arges[16] + arges[17]) / 3, 1))
            if arges[16] != -200:
                self.in_data_num_15.set(round(arges[16], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[17] != -200:
                self.in_data_num_25.set(round(arges[17], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[18] != -200:
                self.in_data_num_06.set(round(arges[18], 1))  # 下面10路平均温度设置，保留1位小数
                self.avg_num_6.set(round((arges[18] + arges[19] + arges[20]) / 3, 1))
            if arges[19] != -200:
                self.in_data_num_16.set(round(arges[19], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[20] != -200:
                self.in_data_num_26.set(round(arges[20], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[21] != -200:
                self.in_data_num_07.set(round(arges[21], 1))  # 下面10路平均温度设置，保留1位小数
                self.avg_num_7.set(round((arges[21] + arges[22] + arges[23]) / 3, 1))
            if arges[22] != -200:
                self.in_data_num_17.set(round(arges[22], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[23] != -200:
                self.in_data_num_27.set(round(arges[23], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[24] != -200:
                self.in_data_num_08.set(round(arges[24], 1))  # 下面10路平均温度设置，保留1位小数
                self.avg_num_8.set(round((arges[24] + arges[25] + arges[26]) / 3, 1))
            if arges[25] != -200:
                self.in_data_num_18.set(round(arges[25], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[26] != -200:
                self.in_data_num_28.set(round(arges[26], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[27] != -200:
                self.in_data_num_09.set(round(arges[27], 1))  # 下面10路平均温度设置，保留1位小数
                self.avg_num_9.set(round((arges[27] + arges[28] + arges[29]) / 3, 1))
            if arges[28] != -200:
                self.in_data_num_19.set(round(arges[28], 1))  # 下面10路平均温度设置，保留1位小数
            if arges[29] != -200:
                self.in_data_num_29.set(round(arges[29], 1))  # 下面10路平均温度设置，保留1位小数

            # self.write_re_log_son(arges)  # 文本展示区 展示
        except Exception as e:
            print('son设置温度错误', e)

    # 10路平均温度框
    def ten_avg(self):
        self.tenAvg_label = Label(self.top, text="平均温度显示", bg="#F0FFFF", font=("楷", 12))  # 平均温度标签
        self.tenAvg_label.place(relx=x1[0], rely=y3[5], anchor=CENTER)
        self.avg_0 = Label(self.top, textvariable=self.avg_num_0, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_0.place(relx=x3[0], rely=y3[6], anchor=CENTER)
        self.avg_1 = Label(self.top, textvariable=self.avg_num_1, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_1.place(relx=x3[1], rely=y3[6], anchor=CENTER)
        self.avg_2 = Label(self.top, textvariable=self.avg_num_2, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_2.place(relx=x3[2], rely=y3[6], anchor=CENTER)
        self.avg_3 = Label(self.top, textvariable=self.avg_num_3, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_3.place(relx=x3[3], rely=y3[6], anchor=CENTER)
        self.avg_4 = Label(self.top, textvariable=self.avg_num_4, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_4.place(relx=x3[4], rely=y3[6], anchor=CENTER)
        self.avg_5 = Label(self.top, textvariable=self.avg_num_5, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_5.place(relx=x3[5], rely=y3[6], anchor=CENTER)
        self.avg_6 = Label(self.top, textvariable=self.avg_num_6, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_6.place(relx=x3[6], rely=y3[6], anchor=CENTER)
        self.avg_7 = Label(self.top, textvariable=self.avg_num_7, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_7.place(relx=x3[7], rely=y3[6], anchor=CENTER)
        self.avg_8 = Label(self.top, textvariable=self.avg_num_8, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_8.place(relx=x3[8], rely=y3[6], anchor=CENTER)
        self.avg_9 = Label(self.top, textvariable=self.avg_num_9, width=w1, height=h1, font=("仿宋", 18),
                           bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.avg_9.place(relx=x3[9], rely=y3[6], anchor=CENTER)

        # self.avg_num_0.set('ok')
        # self.avg_num_1.set('ok')
        # self.avg_num_2.set('ok')
        # self.avg_num_3.set('ok')
        # self.avg_num_4.set('ok')
        # self.avg_num_5.set('ok')
        # self.avg_num_6.set('ok')
        # self.avg_num_7.set('ok')
        # self.avg_num_8.set('ok')
        # self.avg_num_9.set('ok')

    # 更新缓存区
    def update(self):
        global num_updata_in, connect
        # t = time.localtime()
        # t_min = t[4]
        # t_s = t[5]
        if connect:
            try:
                father_data = FATHER(tkinter.Tk).recvdata()  # 父类传过来的接收数据
                self.set_30_data(father_data)  # 接收数据处理函数
                print('父类传过来的%d个温度数据为：%s' % (len(father_data), father_data))
            except Exception as e:
                print(e)
        else:
            print('update 未连接')
        self.window_name.after(num_updata_in, self.update)

    # 温度接收动态打印
    # def write_re_log_son(self, logmsg):
    #     global LOG_RE_NUM, re_log_len
    #     logmsg_in = str(logmsg) + "\n"  # 换行
    #     if LOG_RE_NUM <= re_log_len:
    #         self.recorde.insert(END, logmsg_in)
    #         LOG_RE_NUM = LOG_RE_NUM + 1
    #     else:
    #         self.recorde.delete(1.0, 2.0)  # 将之前的第1、2个数据删掉
    #         self.recorde.insert(END, logmsg_in)

    def in_data(self):
        self.in_data_0_label = Label(self.top, text='0', bg="#F0FFFF", width=w1, font=("仿宋", 18))
        self.in_data_0_label.place(relx=x3[0], rely=y3[0], anchor=CENTER)
        self.in_data_1_label = Label(self.top, text='1', bg="#F0FFFF", width=w1, font=("仿宋", 18))
        self.in_data_1_label.place(relx=x3[1], rely=y3[0], anchor=CENTER)
        self.in_data_2_label = Label(self.top, text='2', bg="#F0FFFF", width=w1, font=("仿宋", 18))
        self.in_data_2_label.place(relx=x3[2], rely=y3[0], anchor=CENTER)
        self.in_data_3_label = Label(self.top, text='3', bg="#F0FFFF", width=w1, font=("仿宋", 18))
        self.in_data_3_label.place(relx=x3[3], rely=y3[0], anchor=CENTER)
        self.in_data_4_label = Label(self.top, text='4', bg="#F0FFFF", width=w1, font=("仿宋", 18))
        self.in_data_4_label.place(relx=x3[4], rely=y3[0], anchor=CENTER)
        self.in_data_5_label = Label(self.top, text='5', bg="#F0FFFF", width=w1, font=("仿宋", 18))
        self.in_data_5_label.place(relx=x3[5], rely=y3[0], anchor=CENTER)
        self.in_data_6_label = Label(self.top, text='6', bg="#F0FFFF", width=w1, font=("仿宋", 18))
        self.in_data_6_label.place(relx=x3[6], rely=y3[0], anchor=CENTER)
        self.in_data_7_label = Label(self.top, text='7', bg="#F0FFFF", width=w1, font=("仿宋", 18))
        self.in_data_7_label.place(relx=x3[7], rely=y3[0], anchor=CENTER)
        self.in_data_8_label = Label(self.top, text='8', bg="#F0FFFF", width=w1, font=("仿宋", 18))
        self.in_data_8_label.place(relx=x3[8], rely=y3[0], anchor=CENTER)
        self.in_data_9_label = Label(self.top, text='9', bg="#F0FFFF", width=w1, font=("仿宋", 18))
        self.in_data_9_label.place(relx=x3[9], rely=y3[0], anchor=CENTER)

        self.in_data_00 = Label(self.top, textvariable=self.in_data_num_00, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_00.place(relx=x3[0], rely=y3[1], anchor=CENTER)
        # self.in_data_num_00.set(24.5)  # 环境温度设置
        self.in_data_01 = Label(self.top, textvariable=self.in_data_num_01, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_01.place(relx=x3[1], rely=y3[1], anchor=CENTER)
        self.in_data_02 = Label(self.top, textvariable=self.in_data_num_02, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_02.place(relx=x3[2], rely=y3[1], anchor=CENTER)
        self.in_data_03 = Label(self.top, textvariable=self.in_data_num_03, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_03.place(relx=x3[3], rely=y3[1], anchor=CENTER)
        self.in_data_04 = Label(self.top, textvariable=self.in_data_num_04, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_04.place(relx=x3[4], rely=y3[1], anchor=CENTER)
        self.in_data_05 = Label(self.top, textvariable=self.in_data_num_05, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_05.place(relx=x3[5], rely=y3[1], anchor=CENTER)
        self.in_data_06 = Label(self.top, textvariable=self.in_data_num_06, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_06.place(relx=x3[6], rely=y3[1], anchor=CENTER)
        self.in_data_07 = Label(self.top, textvariable=self.in_data_num_07, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_07.place(relx=x3[7], rely=y3[1], anchor=CENTER)
        self.in_data_08 = Label(self.top, textvariable=self.in_data_num_08, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_08.place(relx=x3[8], rely=y3[1], anchor=CENTER)
        self.in_data_09 = Label(self.top, textvariable=self.in_data_num_09, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_09.place(relx=x3[9], rely=y3[1], anchor=CENTER)

        self.in_data_10 = Label(self.top, textvariable=self.in_data_num_10, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_10.place(relx=x3[0], rely=y3[2], anchor=CENTER)
        self.in_data_11 = Label(self.top, textvariable=self.in_data_num_11, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_11.place(relx=x3[1], rely=y3[2], anchor=CENTER)
        self.in_data_12 = Label(self.top, textvariable=self.in_data_num_12, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_12.place(relx=x3[2], rely=y3[2], anchor=CENTER)
        self.in_data_13 = Label(self.top, textvariable=self.in_data_num_13, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_13.place(relx=x3[3], rely=y3[2], anchor=CENTER)
        self.in_data_14 = Label(self.top, textvariable=self.in_data_num_14, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_14.place(relx=x3[4], rely=y3[2], anchor=CENTER)
        self.in_data_15 = Label(self.top, textvariable=self.in_data_num_15, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_15.place(relx=x3[5], rely=y3[2], anchor=CENTER)
        self.in_data_16 = Label(self.top, textvariable=self.in_data_num_16, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_16.place(relx=x3[6], rely=y3[2], anchor=CENTER)
        self.in_data_17 = Label(self.top, textvariable=self.in_data_num_17, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_17.place(relx=x3[7], rely=y3[2], anchor=CENTER)
        self.in_data_18 = Label(self.top, textvariable=self.in_data_num_18, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_18.place(relx=x3[8], rely=y3[2], anchor=CENTER)
        self.in_data_19 = Label(self.top, textvariable=self.in_data_num_19, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_19.place(relx=x3[9], rely=y3[2], anchor=CENTER)

        self.in_data_20 = Label(self.top, textvariable=self.in_data_num_20, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_20.place(relx=x3[0], rely=y3[3], anchor=CENTER)
        self.in_data_21 = Label(self.top, textvariable=self.in_data_num_21, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_21.place(relx=x3[1], rely=y3[3], anchor=CENTER)
        self.in_data_22 = Label(self.top, textvariable=self.in_data_num_22, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_22.place(relx=x3[2], rely=y3[3], anchor=CENTER)
        self.in_data_23 = Label(self.top, textvariable=self.in_data_num_23, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_23.place(relx=x3[3], rely=y3[3], anchor=CENTER)
        self.in_data_24 = Label(self.top, textvariable=self.in_data_num_24, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_24.place(relx=x3[4], rely=y3[3], anchor=CENTER)
        self.in_data_25 = Label(self.top, textvariable=self.in_data_num_25, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_25.place(relx=x3[5], rely=y3[3], anchor=CENTER)
        self.in_data_26 = Label(self.top, textvariable=self.in_data_num_26, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_26.place(relx=x3[6], rely=y3[3], anchor=CENTER)
        self.in_data_27 = Label(self.top, textvariable=self.in_data_num_27, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_27.place(relx=x3[7], rely=y3[3], anchor=CENTER)
        self.in_data_28 = Label(self.top, textvariable=self.in_data_num_28, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_28.place(relx=x3[8], rely=y3[3], anchor=CENTER)
        self.in_data_29 = Label(self.top, textvariable=self.in_data_num_29, width=w1, height=h1, font=("仿宋", 18),
                                bg='#FFFAFA', relief='groove', bd=3)  # 0路温度框 不能改变
        self.in_data_29.place(relx=x3[9], rely=y3[3], anchor=CENTER)

        # self.in_data_30 = Label(self.top, textvariable=self.in_data_num_30, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_30.place(relx=x1[0], rely=y1[3], anchor=CENTER)
        # self.in_data_31 = Label(self.top, textvariable=self.in_data_num_31, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_31.place(relx=x1[1], rely=y1[3], anchor=CENTER)
        # self.in_data_32 = Label(self.top, textvariable=self.in_data_num_32, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_32.place(relx=x1[2], rely=y1[3], anchor=CENTER)
        # self.in_data_33 = Label(self.top, textvariable=self.in_data_num_33, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_33.place(relx=x1[3], rely=y1[3], anchor=CENTER)
        # self.in_data_34 = Label(self.top, textvariable=self.in_data_num_34, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_34.place(relx=x1[4], rely=y1[3], anchor=CENTER)
        # self.in_data_35 = Label(self.top, textvariable=self.in_data_num_35, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_35.place(relx=x1[5], rely=y1[3], anchor=CENTER)
        # self.in_data_36 = Label(self.top, textvariable=self.in_data_num_36, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_36.place(relx=x1[6], rely=y1[3], anchor=CENTER)
        # self.in_data_37 = Label(self.top, textvariable=self.in_data_num_37, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_37.place(relx=x1[7], rely=y1[3], anchor=CENTER)
        # self.in_data_38 = Label(self.top, textvariable=self.in_data_num_38, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_38.place(relx=x1[8], rely=y1[3], anchor=CENTER)
        # self.in_data_39 = Label(self.top, textvariable=self.in_data_num_39, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_39.place(relx=x1[9], rely=y1[3], anchor=CENTER)

        # self.in_data_40 = Label(self.top, textvariable=self.in_data_num_40, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_40.place(relx=x1[0], rely=y1[4], anchor=CENTER)
        # self.in_data_41 = Label(self.top, textvariable=self.in_data_num_41, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_41.place(relx=x1[1], rely=y1[4], anchor=CENTER)
        # self.in_data_42 = Label(self.top, textvariable=self.in_data_num_42, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_42.place(relx=x1[2], rely=y1[4], anchor=CENTER)
        # self.in_data_43 = Label(self.top, textvariable=self.in_data_num_43, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_43.place(relx=x1[3], rely=y1[4], anchor=CENTER)
        # self.in_data_44 = Label(self.top, textvariable=self.in_data_num_44, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_44.place(relx=x1[4], rely=y1[4], anchor=CENTER)
        # self.in_data_45 = Label(self.top, textvariable=self.in_data_num_45, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_45.place(relx=x1[5], rely=y1[4], anchor=CENTER)
        # self.in_data_46 = Label(self.top, textvariable=self.in_data_num_46, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_46.place(relx=x1[6], rely=y1[4], anchor=CENTER)
        # self.in_data_47 = Label(self.top, textvariable=self.in_data_num_47, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_47.place(relx=x1[7], rely=y1[4], anchor=CENTER)
        # self.in_data_48 = Label(self.top, textvariable=self.in_data_num_48, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_48.place(relx=x1[8], rely=y1[4], anchor=CENTER)
        # self.in_data_49 = Label(self.top, textvariable=self.in_data_num_49, width=w1, height=h1, font=("仿宋", 18),
        # bg='#FFFAFA', relief='groove', bd =3)  # 0路温度框 不能改变
        # self.in_data_49.place(relx=x1[9], rely=y1[4], anchor=CENTER)


def gui_start():
    init_window = Tk()  # 实例化出一个父窗口
    SET_FATHER = FATHER(init_window)  # 设father根窗口默认属性
    SET_FATHER.set_father_window()
    SET_SON = SON(init_window)  # 设置son窗口默认属性
    SET_SON.set_son_window(init_window)
    init_window.mainloop()  # 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


if __name__ == '__main__':
    gui_start()
