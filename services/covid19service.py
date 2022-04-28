import requests
import re
from bs4 import BeautifulSoup
from services import pttservice
from django_redis import get_redis_connection
import datetime
import json
# fix: InsecureRequestWarning: Unverified HTTPS request is being made to host
import requests.packages.urllib3

url = "https://covid-19.nchc.org.tw/dt_005-covidTable_taiwan.php"


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}


def getCovid19():
    try:
        nowDateEng = datetime.datetime.now().strftime("%b-%-d")
        redisKey = "Covid19:offical:"+nowDateEng
        r = get_redis_connection("heroku")
        keyExist = r.exists(redisKey)
        if keyExist:
            rResult = r.get(redisKey)
            return json.loads(rResult)

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
        # print("totalDeaths ", totalDeaths)
        # 死亡率
        rateDeaths = "0%" if len(soup.select(
            "#country_cfr")) == 0 else soup.select("#country_cfr")[0].text
        m = re.search(r'\d+\.?\d*%?', rateDeaths)
        if m != None:
            rateDeaths = m.group()
        # print("rateDeaths ", rateDeaths)

        # 新增死亡
        newDeaths = "0" if len(soup.select(
            ".country_deaths_change")) == 0 else soup.select(".country_deaths_change")[0].text
        if len(newDeaths.strip()) == 0:
            newDeaths = "0"

        # 新增確診
        recovered = "0" if len(soup.select(
            ".country_recovered")) == 0 else soup.select(".country_recovered")[0].text
        recovered = re.sub("[+,]", "", recovered)

        # 本土
        domesticRecovered = "0" if len(soup.select(
            ".country_confirmed_percent")) < 1 else soup.select(".country_confirmed_percent")[1].text.split("本土病例 ")[1]

        # 本土
        internationalRecovered = str(int(recovered)-int(domesticRecovered))

        # 疫苗接種人次
        vaccine = "0" if len(soup.select(
            ".country_deaths_change")) == 0 else soup.select(".country_deaths")[1].text

        # 疫苗覆蓋率
        vaccinePercent = "0" if len(soup.select(
            ".country_deaths_change")) < 1 else soup.select(".country_deaths_percent")[0].text

        # 本土病例分佈
        # local = "" if len(soup.select(
        #     ".btn btn-success btn-lg")) < 1 else soup.select(".btn btn-success btn-lg")[0].text
        countrys = [] if len(soup.select(".col-lg-12")
                             ) < 1 else soup.select(".col-lg-12")[1]
        countrysDict = {}
        for country in countrys.select("a"):
            countryTodayCount = country.select(
                "span")[1].text.replace(u'\xa0', u'').replace("\n", "")
            # print("countryTodayCount = ", countryTodayCount, "kk")
            if countryTodayCount != "":
                countryTotalCount = country.select(
                    "span")[0].text.split("+")[0]
                countrysDict[countryTotalCount] = countryTodayCount

        result = {
            "url": url,
            "time": time,
            "date": time.split(" ")[2],  # Updated on Apr-28 UTC + 8
            "total": totalConfirmed,
            "recovered": recovered,
            "domesticRecovered": domesticRecovered,
            "internationalRecovered": internationalRecovered,
            "rateDeaths": rateDeaths,
            "newDeaths": newDeaths,
            "totalDeaths": totalDeaths,
            "vaccine": vaccine,
            "vaccinePercent": vaccinePercent,
            "countrysDict": countrysDict
        }

        redisKey = "Covid19:offical:"+result["date"]
        if r.setnx(redisKey, str(result)):
            r.expire(redisKey, 60*60*12)
        print("get ", r.get(redisKey))
        return result
    except Exception as e:
        print(e)
        return ""


def getGossipCovid19():
    # start = 39254  # 設定起始網頁 (務必自行調整)
    # number = 5    # 設定要從開始頁面往後爬多少個
    # end = start - number
    # for i in range(start, end, -1):
    #     # 組成 正確 URL
    #     link = "https://www.ptt.cc/bbs/Gossiping/index"+str(i)+".html"
    #     # 執行單頁面網頁爬蟲
    #     getPTT(link)
    #     # 避免被太快被 PTT 封鎖請求
    #     time.sleep(1)
    link = "https://www.ptt.cc/bbs/Gossiping/"
    regex = re.compile(r'^\[爆卦\] 本.*')
    r = get_redis_connection("heroku")
    date = datetime.datetime.today().strftime("%-m/%d")
    redisKey = "Covid19:ptt:"+date
    keyExist = r.exists(redisKey)
    print("keyExist = ", keyExist)
    if keyExist:
        print("======= Covid19:ptt:%s" % (date))
        rResult = r.get(redisKey)
        return json.loads(rResult)
    result = pttservice.getPTT(link, regex)

    redisKey = "Covid19:ptt:"+result["Date"]
    if r.setnx(redisKey, str(result)):
        r.expire(redisKey, 60*60*12)

    return result


if __name__ == "__main__":
    # print(getCovid19())
    print(getCovid19())
    # print(getGossipCovid19())
