import websocket
import json
import time
from win10toast import ToastNotifier #通知弹窗库
import threading #用于多线程支持
import subprocess #用于启动python

number = 1 #要提取的地震列表（1为最新的）

# 回调函数，处理连接打开
def on_open():
    print("连接已打开")
    #Windows通知弹窗
    toaster = ToastNotifier()
    toaster.show_toast("CENC_eq_notice","程序正在运行，连接已打开",duration=10)

# 回调函数，处理接收到的消息
def on_message(ws, r):
    response = json.loads(r) #将收到的消息解析为json
    print(f"{response}") #打印响应（调试）
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

    #中国地震台网 地震信息
    if type == "cenc_eqlist":
        mag = response[f"No{number}"]["magnitude"] #震级
        location = response[f"No{number}"]["location"] #震源地
        lon = response[f"No{number}"]["longitude"] #经度
        lat = response[f"No{number}"]["latitude"] #纬度
        depth = response[f"No{number}"]["depth"] #震源深
        intensity = response[f"No{number}"]["intensity"] #最大烈度
        eq_time = response[f"No{number}"]["time"] #发震时刻
        type = response[f"No{number}"]["type"] #自动/正式
        
        #格式化输出
        if type == "reviewed":
            type = "中国地震台网速报（正式）"
        else:
            type = "中国地震台网速报（自动）"

        output = f"发震时间：{eq_time},震源:{location}（{lat},{lon}），震级:M{mag}，震源深:{depth}km，最大烈度:{intensity}度"
        message(output,type) #调用通知函数

    #JMA 地震情報
    if type == "query_jmaeqlist":
        mag = response[f"No{number}"]["magnitude"] #震级
        location = response[f"No{number}"]["location"] #震源地
        lon = response[f"No{number}"]["longitude"] #经度
        lat = response[f"No{number}"]["latitude"] #纬度
        depth = response[f"No{number}"]["depth"] #震源深
        shindo = response[f"No{number}"]["shindo"] #最大震度
        eq_time = response[f"No{number}"]["time_full"] #发震时刻
        tsunami = response[f"No{number}"]["info"] #海啸信息

        #格式化输出
        type = "JMA 地震情報"
        output = f"发震时间：{eq_time},震源:{location}（{lat},{lon}），震级:M{mag}，震源深:{depth}，最大震度:{shindo}，{tsunami}"
        message(output,type) #调用通知函数

    #四川地震局 地震预警
    if type == "sc_eew":
        eq_time = response["OriginTime"] #发震时间
        location = response["HypoCenter"] #震源地
        lon = response["Longitude"] #震源地经度
        lat = response["Latitude"] #震源地纬度
        mag = response["Magunitude"] #震级
        #depth = response["Depth"] #震源深度(原报文未提供)
        intensity = response["MaxIntensity"] #最大烈度
        report_num = response["ReportNum"] #EEW发报数

        #格式化输出
        type = f"四川地震局 地震预警 第{report_num}报"
        output = f"发震时间：{eq_time}，震源:{location}（{lat},{lon}），震级:M{mag}，最大烈度:{intensity}"
        message(output,type) #调用通知函数

    #福建地震局 地震预警
    if type == "fj_eew":
        eq_time = response["OriginTime"] #发震时间
        location = response["HypoCenter"] #震源地
        lon = response["Longitude"] #震源地经度
        lat = response["Latitude"] #震源地纬度
        mag = response["Magunitude"] #震级
        report_num = response["ReportNum"] #EEW发报数
        isFinal = response["isFinal"] #是否为最终报
        
        #格式化输出
        if isFinal == True:
            isFinal = "（最终）"
        else:
            isFinal = ""
        
        type = f"福建地震局 地震预警 第{report_num}报{isFinal}"
        output = f"发震时间：{eq_time}，震源:{location}（{lat},{lon}），震级:M{mag}"
        message(output,type)
        
    #JMA 緊急地震速報
    if type == "jma_eew":
        eq_time = response["OriginTime"] #发震时间
        location = response["Hypocenter"] #震源地
        lon = response["Longitude"] #震源地经度
        lat = response["Latitude"] #震源地纬度
        mag = response["Magunitude"] #震级
        depth = response["Depth"] #震源深度
        shindo = response["MaxIntensity"] #最大震度
        type = response["Title"] #EEW发报报头
        report_num = response["Serial"] #EEW发报数
        isAssumption = response["isAssumption"] #是否为推定震源（PLUM/レベル/IPF法）
        isFinal = response["isFinal"] #是否为最终报
        isCancel = response["isCancel"] #是否为取消报
        
        #格式化输出
        if isFinal == True:
            isFinal = "（最终）"
        else:
            isFinal = ""

        if isCancel == True:
            isCancel = "（取消）"
        else:
            isCancel = ""

        if isAssumption == True:
            isAssumption = "推定"
        else:
            isAssumption = ""

        type = f"{type} 第{report_num}报{isFinal}{isCancel}"
        output = f"发震时间：{eq_time}，{isAssumption}震源:{location}（{lat},{lon}），震级:M{mag}，震源深:{depth}km，最大震度:{shindo}"
        message(output,type) #调用通知函数

    #CWA 地震预警
    if type == "cwa_eew":
        eq_time = response["OriginTime"] #发震时间
        location = response["HypoCenter"] #震源地
        report_num = response["ReportNum"] #EEW发报数
        lon = response["Longitude"] #震源地经度
        lat = response["Latitude"] #震源地纬度
        mag = response["Magunitude"] #震级
        depth = response["Depth"] #震源深度
        intensity = response["MaxIntensity"] #最大震度

        #格式化输出
        type = f"CWA 地震预警（第{report_num}报）"
        output = f"发震时间：{eq_time}，震源:{location}（{lat},{lon}），震级:M{mag}，震源深:{depth}km，最大震度:{intensity}"
        message(output,type) #调用通知函数

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

#通知和记录函数
def message(output,type):
    #Windows通知弹窗
    toaster = ToastNotifier()
    toaster.show_toast(f"{type}",f"{output}",duration=10)
    #终端输出
    print(f"{type} {output}")
    #写入文件
    with open("D:\\programing\\python\\eq_weather_notice\\eq_log.txt.txt","a",encoding='utf-8') as file:
        file.write(f"{type} {output}\n")
    #打开记录
    subprocess.call(["python","D:\\programing\\python\\eq_weather_notice\\realtime_sindo.py"])

# WebSocket 客户端线程函数
def start_websocket():
    ws_url = "wss://ws-api.wolfx.jp/all_eew"
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