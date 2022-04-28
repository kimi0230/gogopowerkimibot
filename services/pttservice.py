import requests
import re
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}


def getIndex(soup):
    link = soup.select('.btn.wide')[1].get('href')
    startIndx = link.find('index')
    endIndx = link.find('.html')
    index = link[startIndx+5:endIndx]
    return int(index)+1


def getPTT(url, regex=None, keyword=""):
    try:
        nowIndex = 0
        headers['cookie'] = 'over18=1;'
        if keyword != "":
            url += "search?q="+keyword
        else:
            # 先抓初始頁面的index
            res = requests.get(url+"index.html", headers=headers)
            soup = BeautifulSoup(res.text, "lxml")
            nowIndex = getIndex(soup)
        found = False
        count = 0
        page = 10
        allTitle = []
        while found == False and count <= page:
            if keyword != "":
                tmpurl = "%s&page=%d" % (url, count)
            else:
                tmpurl = "%sindex%d.html" % (url, nowIndex-count)

            res = requests.get(tmpurl, headers=headers)
            # res.encoding = 'UTF-8'
            soup = BeautifulSoup(res.text, "lxml")

            for entry in soup.select('.r-ent'):
                title = entry.select('.title')[0].text.strip()
                date = entry.select('.date')[0].text
                if regex != None:
                    m = regex.match(title)
                    if m != None:
                        found = True
                        link = "https://www.ptt.cc" + \
                            entry.select('a')[0].get('href')
                        return {"Title": title, "Date": date, "Link": link}
                else:
                    allTitle.append(
                        {"Title": title, "Date": date})
            if found == False:
                count += 1
            time.sleep(1)
        if len(allTitle) > 0:
            return allTitle
        else:
            return ""
    except Exception as e:
        print(e)
        return ""


if __name__ == "__main__":
    # 八卦版疫情
    url = "https://www.ptt.cc/bbs/Gossiping/"
    regex = re.compile(r'^\[爆卦\] 本土\+.*')
    print(getPTT(url, regex, "[爆卦] 本土+"))

    # 爬netflix片單
    # url = "https://www.ptt.cc/bbs/EAseries/"
    # regex = re.compile(r'.*Netflix台灣.*片單.*')
    # print(getPTT(url, regex, "Netflix台灣"))
    # print(getPTT(url, regex))
    # print(getPTT(url))
