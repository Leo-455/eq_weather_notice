import websocket
import json
import time
from win10toast import ToastNotifier #通知弹窗库
import sys
import threading  #用于多线程支持

number = 1 #要提取的地震列表（1为最新的）
#sys.stdout.reconfigure(encoding='utf-8') #设置标准输出编码为 UTF-8

# 回调函数，处理连接打开
def on_open(ws):
    print("连接已打开")
#Windows通知弹窗
toaster = ToastNotifier()
toaster.show_toast("CENC_eq_notice","程序正在运行，连接已打开",duration=10)

# 回调函数，处理接收到的消息
def on_message(ws, r):
    response = json.loads(r) #将收到的消息解析为json
    type = response["type"] #提取type字段

    #收到心跳包
    if type == "heartbeat":
        ws.send("ping") #回复ping包
        t = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) #获取当前时间
        print(f"{t} 收到{type}包，ping包已发送") #终端输出

    #收到pong包
    if type == "pong":
        t = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) #获取当前时间
        print(f"{t} 收到{type}包") #终端输出

    #收到地震信息包
    if type == "cenc_eqlist":
        mag = response["type"][f"No{number}"]["magnitude"] #震级
        location = response["type"][f"No{number}"]["location"] #震源地
        lon = response["type"][f"No{number}"]["longitude"] #经度
        lat = response["type"][f"No{number}"]["latitude"] #纬度
        depth = response["type"][f"No{number}"]["depth"] #震源深
        intensity = response["type"][f"No{number}"]["intensity"] #最大烈度
        eq_time = response["type"][f"No{number}"]["time"] #发震时刻
        类别 = response["type"][f"No{number}"]["type"] #自动/正式

        #Windows通知弹窗
        toaster = ToastNotifier()
        toaster.show_toast(f"CENC地震信息（{类别}）",f"发震时间：{eq_time},震源:{location}（{lat},{lon}），震级:M{mag}，震源深:{depth}km，最大烈度:{intensity}度",duration=1)
        #终端输出
        print(f"CENC地震信息（{类别}）,发震时间：{eq_time},震源:{location}（{lat},{lon}），震级:M{mag}，震源深:{depth}km，最大烈度:{intensity}度")

# 回调函数，处理连接关闭
def on_close(ws, close_status_code, close_msg):
    t = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) #获取当前时间
    print(f"{t} 连接已关闭，状态码: {close_status_code}，消息: {close_msg}") #终端输出
    connection = False
    while connection == False:
        time.sleep(5)  #等待5秒后重连
        print("尝试重连...")
        try:
            ws.run_forever()  #重新运行 WebSocket 客户端
            break
        except Exception as e:
            print(f"重连失败: {e}")

# WebSocket 客户端线程函数
def start_websocket():
    ws_url = "wss://ws-api.wolfx.jp/cenc_eqlist"
    ws = websocket.WebSocketApp(
        ws_url,
        on_open=on_open,
        on_message=on_message,
        on_close=on_close
    )
    ws.run_forever()
# 启动 WebSocket 线程
websocket_thread = threading.Thread(target=start_websocket)
websocket_thread.start()