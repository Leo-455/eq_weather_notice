#--coding:UTF-8--
import requests
import json
from plyer import notification
from time import sleep

#CENC API
url = "https://api.wolfx.jp/cenc_eqlist.json"
r = requests.get(url)
    #打印状态码
print(f"状态{r.status_code}")
    #存储并打印结果
response = r.json()
md5 = response["md5"]

#Windows通知弹窗
notification.notify(
    title="程序开始运行",
    message=f"当前md5值：{md5}",
    timeout=5,#弹窗持续时间
    )

md5_new = md5
count = 0

while md5_new == md5:
    sleep(60)
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
    #提取震级、标题、经纬度
    number = 1
    for eq_dict in response:
        mag = response[f"No{number}"]["magnitude"]
        location = response[f"No{number}"]["location"]
        #lon = response[f"No{number}"]["longitude"]暂时用不到
        #lat = response[f"No{number}"]["latitude"]
        depth = response[f"No{number}"]["depth"]
        intensity = response[f"No{number}"]["intensity"]
    
    #Windows通知弹窗
    notification.notify(
        title="CENC地震信息",
        message=f"震源:{location}，震级:M{mag}，震源深:{depth}km，预想烈度:{intensity}度",
        timeout=10,#弹窗持续时间
        )
    #终端输出
    print(f"震源:{location}，震级:M{mag}，震源深:{depth}km，预想烈度:{intensity}度")