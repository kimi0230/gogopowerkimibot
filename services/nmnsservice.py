import requests
from bs4 import BeautifulSoup
import datetime
# from datetime import datetime
from utility import tinyURL
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}


link = "https://www.nmns.edu.tw/learn/feature/star/%s/%s%s/"


def getStar(year="", month=""):
    try:
        nowDate = datetime.datetime.today()
        if year == "":
            year = nowDate.year
        if month == "":
            month = "%02d" % nowDate.month
        else:
            month = "%02d" % month
        url = link % (year, year, month)
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            return None

        soup = BeautifulSoup(res.text, "lxml")

        #  0: 總介紹
        contents = [] if len(soup.select('.ts_overflow_Xh p')
                             ) == 0 else [p.text.strip() for p in soup.select('.ts_overflow_Xh p') if p.text.strip() != ""]

        reg = r"[\u4e00-\u9fa5]{1,2}月[\u4e00 -\u9fa5]{1,2}日"
        contentsTitle = [] if len(soup.select('.bold-title')
                                  ) == 0 else [transZhTime2Arabic(p.text.strip(), reg) for p in soup.select('.bold-title') if p.text.strip() != ""]

        title = soup.select('#content-title h2')[0].text.strip()

        imageRoot = "https://www.nmns.edu.tw"
        images = []if len(soup.select('.ts_overflow_Xh a')
                          ) == 0 else [{"title": a.get("title"), "link": "%s%s" % (imageRoot, a.get("href"))} for a in soup.select('.ts_overflow_Xh a') if a.get("title") != None]

        result = {
            "url": url,
            "title": title,
            "contents": contents[:-2],  # 後面的聯絡資訊不要
            "contentsTitle": contentsTitle,
            "images": images
        }

        return result
    except Exception as e:
        print(e)
        return ""


def getStarText(year="", month=""):
    try:
        starResult = getStar(year, month)
        if starResult == None:
            return None

        msg = starResult['title']+"\t"+starResult['url'] + \
            "\n"+starResult['contents'][0] + "\n\n"

        msg += "\n".join(s['title'] for s in starResult['contentsTitle'])
        return msg
    except Exception as e:
        print(e)
        return None


def getStarDayText(now):
    try:
        nowDate = "%d/%d" % (now.month, now.day)
        starResult = getStar(now.year, now.month)
        if starResult == None:
            return "當日無資料", None

        resMsg = ""
        for i in range(len(starResult['contentsTitle'])):
            if starResult['contentsTitle'][i]['day'] == nowDate:
                resMsg += "%s\n%s\n%s" % (nowDate,
                                          starResult['contents'][2*i+1].split("、")[1], starResult['contents'][2*i+2])
                resImgURL = starResult['images'][i]['link']
                break
        if resMsg == "":
            return "當日無資料", None
        return resMsg, resImgURL
    except Exception as e:
        print(e)
        return None, None


def transZhTime2Arabic(msg, reg):
    # year = str.split('年')[0]
    dateStr = re.search(reg, msg).group()
    month = dateStr.split('月')[0]
    day = dateStr.split('月')[1].split('日')[0]

    NUM = {'零': '0', '一': '1', '二': '2',
           '三': '3', '四': '4', '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '十': '10'}

    if len(day) > 2:
        day = day[0]+day[1]

    month = ''.join(str(NUM[i]) for i in month)
    day = ''.join(str(NUM[i]) for i in day)

    if len(month) == 3:
        month = '1'+month[2]
    if len(day) == 3:
        day = '1'+day[2]
    return{"title": msg.replace(dateStr, month+"/"+day), "day": month+"/"+day}


if __name__ == "__main__":
    # python3 -B -m services.nmnsservice
    now = datetime.datetime.now()
    # getStar()
    getStarDayText(now)
    # transZhTime2Arabic("二、九月九日 水星合月", r"[\u4e00-\u9fa5]+月[\u4e00-\u9fa5]日+")
    # a, b = transZhTime2Arabic(
    #     "二、九月一九日 水星合月", r"[\u4e00-\u9fa5]{1,2}月[\u4e00 -\u9fa5]{1,2}日")
    # print(b)
