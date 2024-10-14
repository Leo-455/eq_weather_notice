#--coding:UTF-8--
import requests #api库
import json
import time
from plyer import notification #通知弹窗库
from time import sleep

count = 0 #重置计数
active = True #初始化活动状态
wait = 60 #初始化等待时间
md5 = 0 #初始化MD5值
url = "https://api.wolfx.jp/cenc_eqlist.json" #CENC API

while active == True: #循环
    md5_new = md5 #重置MD5值
    while md5_new == md5: #循环，判断MD5值是否改变
        try:
            sleep(wait)
            r = requests.get(url) #请求
            response = r.json() #存储
            md5 = response["md5"] #提取新MD5值
            
            #处理异常状态码（未测试）
            if r.status_code != 200:
                print("请求失败，状态码:", r.status_code)
                break  #在请求失败时退出
            
            #处理第一次请求
            if count == 0:
                md5_new = md5 #初始化md5_new
                #Windows通知弹窗
                notification.notify(
                    title = "程序开始运行",
                    message = f"当前md5值：{md5}"
                    )
            
            t = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) #获取当前时间
            print(f"{t} BJT  {count}次  状态码{r.status_code}") #终端状态输出
            count = count+1 #计数加1
        except requests.exceptions.ConnectionError as e: #处理网络中断
            t = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) #获取当前时间
            print(f"{t} 网络连接中断，正在重试...") #终端状态输出
            sleep(wait)  # 等待后重试
            continue  # 继续循环，尝试再次请求
    else:
        #sleep(10) #!!调试的时候防止死循环!!
        #提取震级、标题、经纬度
        number = 1 #要提取的地震列表位置（1为第一个）
        for eq_dict in response:
            mag = response[f"No{number}"]["magnitude"] #震级
            location = response[f"No{number}"]["location"] #震源地
            #lon = response[f"No{number}"]["longitude"]暂时用不到
            #lat = response[f"No{number}"]["latitude"]
            depth = response[f"No{number}"]["depth"] #震源深
            intensity = response[f"No{number}"]["intensity"] #最大烈度
            type = response[f"No{number}"]["type"] #自动/正式
            eq_time = response[f"No{number}"]["time"] #发震时刻

        if type == "reviewed":
            类别 = "正式测定"
            wait = 60

        if type == "automatic":
            类别 = "自动测定"
            wait = 1

        #Windows通知弹窗
        notification.notify(
            title = f"CENC地震信息（{类别}）",
            message = f"发震时间：{eq_time},震源:{location}，震级:M{mag}，震源深:{depth}km，最大烈度:{intensity}度",#这玩意咋换行啊？？？
            timeout = 60, #弹窗持续时间
            )
        #终端输出
        print(f"CENC地震信息（{类别}）,发震时间：{eq_time},震源:{location}，震级:M{mag}，震源深:{depth}km，最大烈度:{intensity}度")