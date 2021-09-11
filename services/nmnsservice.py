
from module import msgresponse
import requests
from bs4 import BeautifulSoup
import datetime

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
        url = link % (year, year, month)
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "lxml")

        #  0: 總介紹
        contents = [] if len(soup.select('.ts_overflow_Xh p')
                             ) == 0 else [p.text.strip() for p in soup.select('.ts_overflow_Xh p') if p.text.strip() != ""]

        contentTitle = soup.select('#content-title h2')[0].text.strip()

        images = []if len(soup.select('.ts_overflow_Xh a')
                          ) == 0 else [{"title": a.get("title"), "link": a.get("href")} for a in soup.select('.ts_overflow_Xh a') if a.get("title") != None]

        result = {
            "url": url,
            "contentTitle": contentTitle,
            "contents": contents[:-2],  # 後面的聯絡資訊不要
            "images": images
        }
        print(result)
        return result
    except Exception as e:
        print(e)
        return ""


def sendStar(event, msg):
    msgresponse.sendText(event, msg)


if __name__ == "__main__":
    # python3 -B -m services.nmnsservice
    getStar()
