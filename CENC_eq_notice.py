#--coding:UTF-8--
import requests #api库
import json
import time
from plyer import notification #通知弹窗库
from time import sleep

#初始请求
sleep(5) #防止开机自启连不上网报错
url = "https://api.wolfx.jp/cenc_eqlist.json" #CENCapi
r = requests.get(url) #存储请求结果
print(f"状态码{r.status_code} 程序开始运行") #打印状态码
response = r.json() #?
md5 = response["md5"] #提取初始MD5

#Windows通知弹窗
notification.notify(
    title="程序开始运行",
    message=f"当前md5值：{md5}",
    timeout=5,#弹窗持续时间(由windows觉得决定，似乎改不了)
    )

count = 0 #重置计数
active = True #初始化活动状态
wait = 60 #初始化等待时间

#得让下面这一段重复运行
while active == True:
    md5_new = md5 #重置MD5值
    while md5_new == md5: #循环，判断MD5值是否改变
        try:
            sleep(wait)
            #CENC API
            url = "https://api.wolfx.jp/cenc_eqlist.json"
            r = requests.get(url)
            if r.status_code != 200:
                print("请求失败，状态码:", r.status_code)
                break  # 可以选择在请求失败时退出
            response = r.json()
            md5 = response["md5"] #提取新MD5值
            t = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            print(f"{t} BJT  {count}次  状态码{r.status_code}")
            count = count+1
        except requests.exceptions.ConnectionError as e:
            t = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
            print(f"{t} 网络连接中断，正在重试...")
            sleep(wait)  # 等待后重试
            continue  # 继续循环，尝试再次请求
    else:
        #sleep(10) #!!调试的时候防止死循环!!
        md5 = response["md5"] #提取新的MD5值
        #提取震级、标题、经纬度
        number = 1
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
            title=f"CENC地震信息（{类别}）",
            message=f"发震时间：{eq_time},震源:{location}，震级:M{mag}，震源深:{depth}km，最大烈度:{intensity}度",#这玩意咋换行啊？？？
            timeout=60, #弹窗持续时间
            )
        #终端输出
        print(f"CENC地震信息（{类别}）,发震时间：{eq_time},震源:{location}，震级:M{mag}，震源深:{depth}km，最大烈度:{intensity}度")