
import requests
from bs4 import BeautifulSoup
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}


def getCPC():
    url = "https://www.cpc.com.tw/GetOilPriceJson.aspx?type=TodayOilPriceString"
    res = requests.get(url, headers=headers)
    res.encoding = 'UTF-8'

    # html to json
    res = json.loads(res.text)
    title = BeautifulSoup(res["UpOrDown_Html"], "lxml").get_text()
    date = res["PriceUpdate"]
    gasNames = ["92無鉛", "95無鉛", "98無鉛", "酒精汽油", "超級柴油", "液化石油氣"]
    gasList = [{"name": v, "price": res["sPrice" +
                                        str(k+1)]}for k, v in enumerate(gasNames)]
    return {"Title": title, "Data": gasList, "Date": date}


def getPresume():
    try:
        url = "https://gasoline.weiyuan.com.tw/"
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            return None

        res.encoding = 'UTF-8'

        soup = BeautifulSoup(res.text, "lxml")

        # 預估下週油價
        title = soup.select('.h4.pull-left.page-title.mt-0')[0].text
        gasChange, _, dieselChange, _ = [item.text for item in soup.select(
            '.text-center.mt-3 > span')][:4]

        # 今日中油油價
        now98, now95, now92, nowDiesel = [item.text for item in soup.select(
            '.counter.text-dark')][:4]

        # 本週原油
        nowCrude, nowExchange, preCrude, preExchage = [item.text for item in soup.select(
            '.h2.text-primary')][:4]

        result = {
            "Title": title,
            "GasChange": gasChange,
            "DieselChange": dieselChange,
            "Now98": now98,
            "Now95": now95,
            "Now92": now92,
            "NowDiesel": nowDiesel,
            "NowCrude": nowCrude,
            "NowExchange": nowExchange,
            "PreCrude": preCrude,
            "PreExchage": preExchage,
            "URL": url}

        return result
    except Exception as e:
        print(e)
        return None


def getPresumeText():
    try:
        source = getPresume()
        resMsg = ""
        if source != None:
            resMsg = "%s\t\n汽油預估:%s\n柴油預估:%s\n\n今日油價:\n98: %s\t 95: %s\n92: %s\t 柴油: %s\n本週原油: %s\t 本週匯率: %s\n上週原油: %s\t 上週匯率: %s\n" % (
                source["Title"], source["GasChange"], source["DieselChange"], source["Now98"], source["Now95"], source["Now92"], source["NowDiesel"], source["NowCrude"], source["NowExchange"], source["PreCrude"], source["PreExchage"])
            return resMsg
        else:
            return None
    except Exception as e:
        print(e)
        return None


def getCPCText(tomorrow=None):
    try:
        source = getCPC()
        resMsg = ""
        if source != "":
            if tomorrow != None and "%s月%s日" % (tomorrow.month, tomorrow.day) != source["Date"]:
                source["Date"] = "\n%s\n\n%s" % (
                    "(⊙▂⊙ ) 中油還沒更新 ", source["Date"])

            resMsg = "%s\t%s\n" % (
                source["Date"], source["Title"])
            for v in source["Data"]:
                resMsg += "%s : %s \n" % (v["name"], v["price"])
            resMsg += "https://www.cpc.com.tw/"
            return resMsg
        else:
            return None
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    # print(getCPCText())
    print(getPresumeText())
