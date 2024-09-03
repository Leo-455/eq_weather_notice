#--coding:UTF-8--
import requests #api库
import json
from plyer import notification #通知弹窗库
from time import sleep

#初始请求
url = "https://api.wolfx.jp/cenc_eqlist.json" #CENCapi
r = requests.get(url) #打印状态码
print(f"状态{r.status_code}") #存储并打印结果
response = r.json()

md5 = response["md5"] #提取初始MD5

#Windows通知弹窗
notification.notify(
    title="程序开始运行",
    message=f"当前md5值：{md5}",
    timeout=5,#弹窗持续时间
    )

md5_new = md5 #重置MD5值
count = 0 #重置计数
active = True #重置活动状态

#得让下面这一段重复运行
while active == True:
    while md5_new == md5: #循环，判断MD5值是否改变
        sleep(30)
        #CENC API
        url = "https://api.wolfx.jp/cenc_eqlist.json"
        r = requests.get(url)
        #打印状态码
        print(f"状态{r.status_code}")
        #存储并打印结果
        response = r.json()
        md5 = response["md5"]
        print(count)
        count = count+1
        
    else:
        #sleep(10)
        #提取震级、标题、经纬度
        number = 1
        for eq_dict in response:
            mag = response[f"No{number}"]["magnitude"] #震级
            location = response[f"No{number}"]["location"] #标题
            #lon = response[f"No{number}"]["longitude"]暂时用不到
            #lat = response[f"No{number}"]["latitude"]
            depth = response[f"No{number}"]["depth"] #震源深
            intensity = response[f"No{number}"]["intensity"] #预想烈度
            type = response[f"No{number}"]["type"] #自动/正式

        if type == "reviewed":
            类别 = "正式测定"
        else:
            类别 = "自动测定"

        #Windows通知弹窗
        notification.notify(
            title=f"CENC地震信息（{类别}）",
            message=f"震源:{location}，震级:M{mag}，震源深:{depth}km，预想烈度:{intensity}度",
            timeout=60, #弹窗持续时间
            )
        #终端输出
        print(f"震源:{location}，震级:M{mag}，震源深:{depth}km，预想烈度:{intensity}度")    