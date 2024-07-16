#--coding:UTF--
import requests
import json
#from plyer import notification
from time import sleep

#CENC API
url = "https://api.wolfx.jp/cenc_eqlist.json"
r = requests.get(url)
    #打印状态码
print(f"状态{r.status_code}")
    #存储并打印结果
response = r.json()
md5 = response["md5"]

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
    mags,titles,lons,lats,depths = [],[],[],[],[]
    for eq_dict in response:
        mag = response[f"No{number}"]["magnitude"]
        title = response[f"No{number}"]["location"]
        lon = response[f"No{number}"]["longitude"]
        lat = response[f"No{number}"]["latitude"]
        depth = response[f"No{number}"]["depth"]
        mags.append(float(mag)) #源文件是字符串，转成浮点型
        titles.append(title)
        lons.append(float(lon)) #源文件是字符串，转成浮点型
        lats.append(float(lat)) #源文件是字符串，转成浮点型
        depths.append(float(depth)) #源文件是字符串，转成浮点型
    
    notification.notify(
        title = "titles",
    )