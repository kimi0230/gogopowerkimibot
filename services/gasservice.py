
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


def getCPCText():
    try:
        source = getCPC()
        resMsg = ""
        if source != "":
            resMsg = "%s\t%s\n" % (
                source["Date"], source["Title"])
            for v in source["Data"]:
                resMsg += "%s : %s \n" % (v["name"], v["price"])
            return resMsg
        else:
            return None
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    print(getCPCText())
