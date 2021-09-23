import requests
import re
from bs4 import BeautifulSoup

# fix: InsecureRequestWarning: Unverified HTTPS request is being made to host
import requests.packages.urllib3
from utility import tinyURL

url = "https://dictionary.cambridge.org/zht"


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}


def transWord(word=None):
    try:
        if word == None:
            return None
        word = word.strip()
        wordURL = 'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/'+word
        res = requests.get(wordURL, headers=headers)
        soup = BeautifulSoup(res.text, "lxml")
        result = {}
        result["Word"] = word
        result["Head"] = []
        result["URL"] = wordURL
        # 詞性, 發音
        for head in soup.select(".pos-header.dpos-h"):
            # 詞性
            partofspeech = head.select('.pos.dpos')[0].text
            # kk 音標
            kk = head.select('.ipa.dipa.lpr-2.lpl-1')
            uk = "[ %s ]" % (kk[0].text)
            ukAudio = url + \
                head.select('source')[0].get("src")
            if len(kk) > 1:
                us = "[ %s ]" % (kk[1].text)
            else:
                us = uk
            usAudio = url + \
                head.select('source')[2].get("src")
            result["Head"].append(
                {"uk": uk, "ukAudio": ukAudio, "us": us, "usAudio": usAudio, "partofspeech": partofspeech})

        if len(result["Head"]) <= 0:
            return None

        # 中文意思
        chtTranslation = set(soup.select(".trans.dtrans.dtrans-se.break-cj")) - \
            set(soup.select(".trans.dtrans.dtrans-se.hdb.break-cj"))
        result["ChtTrans"] = [item.get_text().strip()
                              for item in chtTranslation]

        # 英文意思
        engTranslation = soup.select(".ddef_h")
        result["EngTrans"] = [item.get_text().strip()
                              for item in engTranslation]

        # 例子
        example = soup.select(".examp.dexamp")
        result["Example"] = [item.get_text().strip() for item in example]

        return result
    except Exception as e:
        print(e)
        return None


def getDailyAWord():
    try:
        res = requests.get(url, headers=headers)
        res.encoding = 'UTF-8'
        soup = BeautifulSoup(res.text, "lxml")
        word = soup.select(".fs36.lmt-5.feature-w-big.wotd-hw a")[0].text
        return transWord(word)
    except:
        return ""


def toMsg(source=None, examp=True):
    try:
        if source != None:
            result = "\n%s\n%s\n" % (
                source["Word"], tinyURL.makeTiny(source["URL"]))
            for head in source["Head"]:
                result += "%s\n UK : %s US: %s \n" % (
                    head["partofspeech"], head["uk"], head["us"])
            result += "---------\n"
            for k, v in enumerate(source["ChtTrans"]):
                result += "%s \n %s  \n" % (v, source["EngTrans"][k])
            if examp == True:
                result += "\n---------\n"
                result += "\nExample:\n "+"\n\n".join(source["Example"])
        else:
            return None
        return result
    except:
        return None


if __name__ == "__main__":
    print(getDailyAWord())
