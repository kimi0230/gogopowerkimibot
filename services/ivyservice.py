
import requests
from django.conf import settings
from decouple import config
from bs4 import BeautifulSoup
from utility import tinyURL

ANALYSIS_URL = "https://www.ivy.com.tw/newsLetter/getLifeList"


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
    "content-type": "application/x-www-form-urlencoded; charset = UTF-8"
}

DEFAULTNUMS = 5


def getLastNumsDays(url=ANALYSIS_URL, nums=DEFAULTNUMS):
    try:
        payload = {"_token": "OlYx5mssjNM2uRqpKWVLh8JiyNp1EmLu65lzTwH7",
                   "method": "analysis_list", "currentPageNum": "1",
                   "count": "21"}

        res = requests.post(url, headers=headers, data=payload)
        rawHtml = eval(res.text)[0].replace('\/', '/')

        soup = BeautifulSoup(rawHtml+"</body></html>", "lxml")

        articalList = soup.select("a.list_title")
        if len(articalList) <= 0:
            return None

        result = []
        for i in articalList[:nums]:
            date = i.findChild("p", {"class": "date"}).text[:4]
            week = i.findChild("p", {"class": "date"}).text[4:]
            tmp = {
                "Date": date+" "+week,
                "Title": i.findChild("h6", {"class": "word_title"}).text,
                "Link": tinyURL.makeTiny(i['href'])
            }
            result.append(tmp)

        return result

        # print(articles[0])
    except Exception as e:
        print(e)
        return None


def getLastNumsDaysText(url=ANALYSIS_URL, nums=DEFAULTNUMS):
    try:
        source = getLastNumsDays(url, nums)
        portal = "https://www.ivy.com.tw/newsLetter/portal"
        quiz = "https://www.ivy.com.tw/member/index#"
        resMsg = ""
        if source != None:
            for item in source:
                resMsg += "%s: %s: %s\n" % (
                    item["Date"], item["Title"], item["Link"])
            resMsg += "\nportal:%s\nquiz:%s" % (portal, quiz)
            return resMsg
        else:
            return None
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    print(getLastNumsDaysText(ANALYSIS_URL, DEFAULTNUMS))
