import requests
from django.conf import settings

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

# user_key = settings.CWB_TOKEN
user_key = "CWB-45B26441-4D78-4584-81F8-4A0F93B75DC1"
url = "http://opendata.cwb.gov.tw/opendataapi?dataid=%s&authorizationkey=%s"

cities = ["臺北", "新北", "桃園", "臺中", "臺南", "高雄", "基隆", "新竹", "嘉義"]  # 市
counties = ["苗栗", "彰化", "南投", "雲林", "嘉義", "屏東",
            "宜蘭", "花蓮", "臺東", "澎湖", "金門", "連江"]  # 縣


def getWeather(msg="新北"):
    if not msg == '':  # 天氣類地點存在
        msg = msg.replace('台', '臺')  # 氣象局資料使用「臺」
        matching = [item for item in cities if item in msg]
        flagcity = False  # 檢查是否為縣市名稱
        if len(matching) > 0:
            flagcity = True
        else:
            matching = [item for item in counties if item in msg]
            if len(matching) > 0:
                flagcity = True
            else:
                return ""

        city = matching[0]
        doc_name = "F-C0032-001"
        if city in cities:  # 加上「市」
            city += '市'
            flagcity = True
        elif city in counties:  # 加上「縣」
            city += '縣'
            flagcity = True

        if flagcity:  # 是縣市名稱
            weather = city + '天氣資料：\n'
            # 由氣象局API取得氣象資料
            api_link = url % (doc_name, user_key)
            report = requests.get(api_link).text
            xml_namespace = "{urn:cwb:gov:tw:cwbcommon:0.1}"
            root = et.fromstring(report)
            dataset = root.find(xml_namespace + 'dataset')
            locations_info = dataset.findall(xml_namespace + 'location')
            target_idx = -1

            # 取得 <location> Elements,每個 location 就表示一個縣市資料
            for idx, ele in enumerate(locations_info):
                locationName = ele[0].text  # 取得縣市名
                if locationName == city:
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
            print(weather)
            return weather
        else:
            return ""
    else:
        return ""


if __name__ == "__main__":
    getWeather()
