
from bs4 import BeautifulSoup

# fix: InsecureRequestWarning: Unverified HTTPS request is being made to host
import requests.packages.urllib3

# 測試table
# import prettytable as pt

url = "https://rate.bot.com.tw/xrt?Lang=zh-TW"


herders = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}

defaultCurrency = ["美金 (USD)", "日圓 (JPY)", "英鎊 (GBP)", "人民幣 (CNY)", "歐元 (EUR)"]
allCurrency = [
    "美金 (USD)",
    "港幣 (HKD)",
    "英鎊 (GBP)",
    "澳幣 (AUD)",
    "加拿大幣 (CAD)",
    "新加坡幣 (SGD)",
    "瑞士法郎 (CHF)",
    "日圓 (JPY)",
    "南非幣 (ZAR)",
    "瑞典幣 (SEK)",
    "紐元 (NZD)",
    "泰幣 (THB)",
    "菲國比索 (PHP)",
    "印尼幣 (IDR)",
    "歐元 (EUR)",
    "韓元 (KRW)",
    "越南盾 (VND)",
    "馬來幣 (MYR)",
    "人民幣 (CNY)",
]


def getBoTExchange(msg=""):
    try:
        if msg != "":
            msg = msg.upper()
            for a in allCurrency:
                if msg in a:
                    msg = a
                    found = True
                    break
            if not found:
                return None

        # fix: InsecureRequestWarning: Unverified HTTPS request is being made to host
        requests.packages.urllib3.disable_warnings()
        res = requests.get(url, headers=herders, verify=False)
        res.encoding = 'UTF-8'
        soup = BeautifulSoup(res.text, "lxml")

        time = soup.find(
            "span", class_="time").text.strip()

        table = [s for s in soup.select("table.table tbody tr")]

        queryResult = {}
        for t in table:
            currency = t.select("td div.visible-phone")[0].text.strip()
            cashRateBuy = t.select("td")[1].text.strip()
            cashRateSell = t.select("td")[2].text.strip()
            spotRateBuy = t.select("td")[3].text.strip()
            spotRateSell = t.select("td")[4].text.strip()
            queryResult[currency] = [cashRateBuy,
                                     cashRateSell, spotRateBuy, spotRateSell]

        result = {}
        if msg == "":
            # 只抓預設值
            result = {d: queryResult[d] for d in defaultCurrency}
        else:
            result = {msg: queryResult[msg]}

        if len(result) > 0:
            return result

        return None
    except:
        return None


def toMsg(source=None):
    try:
        if source != None:
            resMsg = "|幣別\t\t|即期買\t|即期賣\t|\n"
            for r in source:
                resMsg += "|%s | %s | %s |\n" % (
                    r, source[r][2], source[r][3])
            resMsg += "https://rate.bot.com.tw/xrt?Lang=zh-TW"
            return resMsg
        else:
            return None
    except:
        return None


if __name__ == "__main__":
    print(toMsg(getBoTExchange()))
