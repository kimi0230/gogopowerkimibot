import requests
import re
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}


def getPTT(url, regex, keyword=""):
    try:
        if keyword != "":
            url += "search?q="+keyword
        headers['cookie'] = 'over18=1;'
        found = False
        count = 1
        page = 5

        while found == False and count <= page:
            if keyword != "":
                tmpurl = "%s&page=%d" % (url, count)
            else:
                tmpurl = url

            res = requests.get(tmpurl, headers=headers)
            # res.encoding = 'UTF-8'
            soup = BeautifulSoup(res.text, "lxml")
            for entry in soup.select('.r-ent'):
                title = entry.select('.title')[0].text.strip()
                m = regex.match(title)
                if m != None:
                    date = entry.select('.date')[0].text
                    link = "https://www.ptt.cc" + \
                        entry.select('a')[0].get('href')
                    found = True
                    return {"Title": title, "Date": date, "Link": link}
            if found == False:
                count += 1
            time.sleep(1)
        return ""
    except:
        return ""


if __name__ == "__main__":
    # 八卦版疫情
    # url = "https://www.ptt.cc/bbs/Gossiping/"
    # regex = re.compile(r'^\[爆卦\] 本土\+.*')
    # print(getPTT(url, regex, "[爆卦] 本土+"))

    # 爬netflix片單
    url = "https://www.ptt.cc/bbs/EAseries/"
    regex = re.compile(r'.*Netflix台灣.*片單.*')
    print(getPTT(url, regex, "Netflix台灣"))
