#--coding:UTF-8--
import requests #api库
import json
from plyer import notification #通知弹窗库
from time import sleep

#初始请求
sleep(5) #防止开机自启连不上网报错
url = "https://api.wolfx.jp/cenc_eqlist.json" #CENCapi
r = requests.get(url) #存储请求结果
print(f"状态{r.status_code}") #打印状态码
response = r.json()
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
        sleep(wait)
        #CENC API
        url = "https://api.wolfx.jp/cenc_eqlist.json"
        r = requests.get(url)
        #打印状态码
        print(f"状态{r.status_code}")
        #存储并打印结果
        response = r.json()
        md5 = response["md5"] #提取信MD5值
        print(count)
        count = count+1
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
            time = response[f"No{number}"]["time"] #发震时刻

        if type == "reviewed":
            类别 = "正式测定"
            wait = 60
        
        if type == "automatic":
            类别 = "自动测定"
            wait = 1
            
        #Windows通知弹窗
        notification.notify(
            title=f"CENC地震信息（{类别}）",
            message=f"发震时间：{time},震源:{location}，震级:M{mag}，震源深:{depth}km，最大烈度:{intensity}度",#这玩意咋换行啊？？？
            timeout=60, #弹窗持续时间
            )
        #终端输出
        print(f"震源:{location}，震级:M{mag}，震源深:{depth}km，最大烈度:{intensity}度")