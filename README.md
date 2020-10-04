# tkinter_GUI
多线程用于接收串口发过来的数据。

 - [串口demo界面截图](https://github.com/WeiFeiLong/tkinter_GUI/blob/master/image/demo.jpg)
 - [网口demo界面截图](https://github.com/WeiFeiLong/tkinter_GUI/blob/master/image/demo_net.jpg)


# 关于代码

 - 串口相关的代码是[serial.py](https://github.com/WeiFeiLong/tkinter_GUI/blob/master/serial.py)和[SerialClass.py](https://github.com/WeiFeiLong/tkinter_GUI/blob/master/SerialClass.py)。
其中SerialClass.py是串口配置部分。直接运行serial.py即可展现出串口GUI。
- 网口相关的代码是[network.py](https://github.com/WeiFeiLong/tkinter_GUI/blob/master/network.py)。直接运行network.py即可展现出网口GUI（客户端）；[server.py](https://github.com/WeiFeiLong/tkinter_GUI/blob/master/server.py)。直接运行server.py即可展现出网口GUI（服务端）。


# 关于GUI界面使用

 - 串口GUI使用
 - 网口GUI使用
首先运行服务端，点击连接；之后运行客户端，点击连接。在日志串口显示连接成功即代表握手成功，可以传输数据了，可以试试在服务端发送[test.txt](https://github.com/WeiFeiLong/tkinter_GUI/blob/master/test.txt)中的数据进行测试。