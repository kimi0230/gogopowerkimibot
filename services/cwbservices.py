import requests
from django.conf import settings
from decouple import config

try:
    from myconst import cityareaconst
except ImportError:
    from ..myconst import cityareaconst
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

try:
    user_token = settings.CWB_TOKEN
except:
    user_token = config('CWB_TOKEN')
cwburl = "http://opendata.cwb.gov.tw/opendataapi?dataid=%s&authorizationkey=%s"

try:
    epa_token = settings.EPA_TOKEN
except:
    epa_token = config('EPA_TOKEN')
epaUrl = "https://data.epa.gov.tw/api/v1/aqx_p_432?limit=1000&api_key=%s&sort=ImportDate desc&format=json"


def getCityArea(msg):
    city = ""
    area = ""
    if not msg == '':
        # 找縣市
        msg = msg.replace('台', '臺')  # 氣象局資料使用「臺」
        for c in cityareaconst.CITY_AREA_MAPPING:
            if c["CityName"] in msg:
                city = c["CityName"]
                matchingCity = c
                break
        if city == "":
            for c in cityareaconst.CITY_AREA_MAPPING:
                if c["CityName2"] in msg:
                    city = c["CityName"]
                    matchingCity = c
                    break

        # 找區鄉鎮
        if city != "":
            matchingArea = [item for item in matchingCity
                            ["AreaList"] if item["AreaName"] in msg or item["AreaName2"] in msg]
            if len(matchingArea) > 0:
                area = matchingArea[0]["AreaName2"]
        else:
            for c in cityareaconst.CITY_AREA_MAPPING:
                for a in c["AreaList"]:
                    if a["AreaName"] in msg or a["AreaName2"] in msg:
                        area = a["AreaName2"]
                        city = c["CityName"]
                        break

    return {"City": city, "Area": area}


def getWeather(msg):
    if not msg == '':  # 天氣類地點存在
        weather = msg + '天氣資料：\n'
        doc_name = "F-C0032-001"
        # 由氣象局API取得氣象資料
        api_link = cwburl % (doc_name, user_token)
        report = requests.get(api_link).text
        xml_namespace = "{urn:cwb:gov:tw:cwbcommon:0.1}"
        root = et.fromstring(report)
        dataset = root.find(xml_namespace + 'dataset')
        locations_info = dataset.findall(xml_namespace + 'location')
        target_idx = -1

        # 取得 <location> Elements,每個 location 就表示一個縣市資料
        for idx, ele in enumerate(locations_info):
            locationName = ele[0].text  # 取得縣市名
            if locationName == msg:
                target_idx = idx
                break
        # 挑選出目前想要 location 的氣象資料
        tlist = ['天氣狀況', '最高溫', '最低溫', '舒適度', '降雨機率']
        for i in range(5):
            element = locations_info[target_idx][i+1]  # 取出 Wx (氣象描述)
            timeblock = element[1]  # 取出目前時間點的資料
            data = timeblock[2][0].text
            weather = weather + tlist[i] + '：' + data + '\n'
        weather = weather[:-1]  # 移除最後一個換行
        return weather
    else:
        return ""


def getAir(msg):
    if not msg == '':  # 天氣類地點存在
        api_link = epaUrl % (epa_token)
        report = requests.get(api_link).json()
        result = ""
        for item in report["records"]:
            if item["SiteName"] == msg:
                result += msg+"空氣品質: \n" + "空氣狀態 : " + item["Status"] + '\n'+"AQI : "+item["AQI"] + \
                    '\n' + "PM2.5 : " + item["PM2.5_AVG"]
                break
        return result


if __name__ == "__main__":
    # getWeather()
    # getAir()
    msg = "板橋"
    cityArea = getCityArea(msg)
    print("cityArea : ", cityArea)
    resMsg = ""
    resMsg += getWeather(cityArea["City"])+"\n\n"
    if cityArea["Area"] != "":
        resMsg += getAir(cityArea["Area"])
    print(resMsg)
    pass
