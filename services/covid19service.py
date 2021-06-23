import requests
import re
from bs4 import BeautifulSoup
import time

# fix: InsecureRequestWarning: Unverified HTTPS request is being made to host
import requests.packages.urllib3

url = "https://covid-19.nchc.org.tw/dt_005-covidTable_taiwan.php"


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}


def getCovid19():
    try:
        # fix: InsecureRequestWarning: Unverified HTTPS request is being made to host
        requests.packages.urllib3.disable_warnings()

        # 台灣疫情報告
        res = requests.get(url, headers=headers, verify=False)
        res.encoding = 'UTF-8'
        soup = BeautifulSoup(res.text, "lxml")
        time = soup.find(
            "span", style="font-size: 0.8em; color: #333333; font-weight: 500;").text.strip()
        totalConfirmed = "0" if len(soup.select(
            ".country_confirmed")) == 0 else soup.select(".country_confirmed")[0].text

        # 累積死亡
        totalDeaths = "0" if len(soup.select(
            ".country_deaths")) == 0 else soup.select(".country_deaths")[0].text

        # 死亡率
        rateDeaths = "0%" if len(soup.select(
            "#country_cfr")) == 0 else soup.select("#country_cfr")[0].text
        m = re.search(r'\d+\.?\d*%?', rateDeaths)
        if m != None:
            rateDeaths = m.group()

        # 新增死亡
        newDeaths = "0" if len(soup.select(
            ".country_deaths_change")) == 0 else soup.select(".country_deaths_change")[0].text
        if len(newDeaths.strip()) == 0:
            newDeaths = "0"

        # 新增確診
        recovered = "0" if len(soup.select(
            ".country_recovered")) == 0 else soup.select(".country_recovered")[0].text

        # 疫苗接種人次
        vaccine = "0" if len(soup.select(
            ".country_deaths_change")) == 0 else soup.select(".country_deaths")[1].text

        result = {
            "url": url,
            "time": time,
            "total": totalConfirmed,
            "recovered": recovered,
            "rateDeaths": rateDeaths,
            "newDeaths": newDeaths,
            "totalDeaths": totalDeaths,
            "vaccine": vaccine,
        }
        return result
    except:
        return ""


def getPTT(url, keyword=""):
    if keyword != "":
        url += "search?q="+keyword
    headers['cookie'] = 'over18=1;'
    found = False
    count = 1
    page = 1
    while found == False and count <= page:
        if keyword != "":
            tmpurl = "%s&page=%d" % (url, count)
        else:
            tmpurl = url

        res = requests.get(tmpurl, headers=headers)
        # res.encoding = 'UTF-8'
        soup = BeautifulSoup(res.text, "lxml")
        for entry in soup.select('.r-ent'):
            title = entry.select('.title')[0].text
            print(title)
            m = re.match(r'\[.*\].*', title)
            print(m)
            if m != None:
                date = entry.select('.date')[0].text
                link = entry.select('a')[0].get('href')
                print(title, date, link)
                found = True
                return {"Title": title, "Date": date, "Link": link}
        if found == False:
            count += 1


def getGossipCovid19():
    start = 39254  # 設定起始網頁 (務必自行調整)
    number = 5    # 設定要從開始頁面往後爬多少個
    end = start - number

    # for i in range(start, end, -1):
    #     # 組成 正確 URL
    #     link = "https://www.ptt.cc/bbs/Gossiping/index"+str(i)+".html"
    #     # 執行單頁面網頁爬蟲
    #     getPTT(link)
    #     # 避免被太快被 PTT 封鎖請求
    #     time.sleep(1)

    link = "https://www.ptt.cc/bbs/Gossiping/"
    getPTT(link, "[爆卦] 本土+")


if __name__ == "__main__":
    # print(getCovid19())
    print(getGossipCovid19())
