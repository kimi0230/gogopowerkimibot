from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from django.conf import settings
from decouple import config
from utility import tinyURL
import re
from services import pttservice, gasservice, cambridgeservice, invoiceservice, nmnsservice
import shutil
import datetime
from services import covid19service

import random
try:
    token = settings.ZHIZHI_NOTIFY_TOKEN
except:
    # for local test
    token = config('ZHIZHI_NOTIFY_TOKEN')

try:
    carbeToken = settings.CARBE_NOTIFY_TOKEN
except:
    carbeToken = config('CARBE_NOTIFY_TOKEN')

try:
    etenToken = settings.ETEN_NOTIFY_TOKEN
except:
    etenToken = config('ETEN_NOTIFY_TOKEN')

try:
    chocoToken = settings.CHOCO_NOTIFY_TOKEN
except:
    chocoToken = config('CHOCO_NOTIFY_TOKEN')
try:
    netflixGrupToken = settings.NETFLIXGRUP_NOTIFY_TOKEN
except:
    netflixGrupToken = config('NETFLIXGRUP_NOTIFY_TOKEN')


bankAccount = config('RICHART_ACCOUNT')
bankAccountLink = config('RICHART_ACCOUNT_LINK')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}


def sendLineNotify(token, params=None, file=None):
    headers = {
        "Authorization": "Bearer " + token,
        # "Content-Type": "application/x-www-form-urlencoded"
    }

    if params == None:
        notify = requests.post(
            "https://notify-api.line.me/api/notify", headers=headers, files=file)
    else:
        notify = requests.post(
            "https://notify-api.line.me/api/notify", headers=headers, params=params, files=file)
    return notify


def test():
    msg = '起床尿尿摟'
    payload = {'message': msg}

    res = sendLineNotify(token, payload)
    if res.status_code == 200:
        print('發送 LINE Notify 成功！')
    else:
        print('發送 LINE Notify 失敗！')


def carbe():
    msg = '卡比起床尿尿'
    payload = {'message': msg}
    res = sendLineNotify(carbeToken, payload)
    if res.status_code == 200:
        print('發送 LINE Notify 成功！')
    else:
        print('發送 LINE Notify 失敗！')


def starDay():
    now = datetime.datetime.now()
    # 找明天
    tomorrow = now + datetime.timedelta(days=1)
    tomorrowDate = "%d/%d" % (tomorrow.month, tomorrow.day)
    starResult = nmnsservice.getStar(tomorrow.year, tomorrow.month)
    if starResult == "":
        return
    # print(starResult)
    resMsg = ""
    for i in range(len(starResult['contentsTitle'])):
        if starResult['contentsTitle'][i]['day'] == tomorrowDate:
            resMsg += "%s\n%s\n%s" % (tomorrowDate,
                                      starResult['contents'][2*i+1].split("、")[1], starResult['contents'][2*i+2])
            resImgURL = starResult['images'][i]['link']
            resImg = requests.get(resImgURL, headers=headers, stream=True)
            break
    if resMsg == "":
        return

    payload = {'message': resMsg}
    file = {'imageFile': resImg.raw}

    tokens = [token]
    with ThreadPoolExecutor(max_workers=3) as executor:
        outStr = []
        for v in tokens:
            res = executor.submit(sendLineNotify, v, payload, file)
            outStr.append(res)

        for future in as_completed(outStr):
            if future.result().status_code == 200:
                print('發送 LINE Notify 成功！')
            else:
                print('發送 LINE Notify 失敗！')
    return


def star():
    try:
        now = datetime.datetime.now()
        year = now.year
        month = now.month

        # 找下一個月
        month += 1
        if month == 13:
            month = 1
            year += 1

        resMsg = nmnsservice.getStarText(year, month)
        if resMsg == "":
            return

        payload = {'message': resMsg}

        tokens = [token, chocoToken]
        # tokens = [token]
        with ThreadPoolExecutor(max_workers=3) as executor:
            outStr = []
            for v in tokens:
                res = executor.submit(sendLineNotify, v, payload)
                outStr.append(res)

            for future in as_completed(outStr):
                if future.result().status_code == 200:
                    print('發送 LINE Notify 成功！')
                else:
                    print('發送 LINE Notify 失敗！')
        return
    except:
        return


def covid19():
    try:
        pttRes = covid19service.getGossipCovid19()
        resMsg = ""
        if pttRes != "":
            resMsg = "%s\n%s\n%s\n" % (
                pttRes["Date"], pttRes["Title"], pttRes["Link"])
        if resMsg == "":
            return

        payload = {'message': resMsg}

        tokens = [carbeToken, etenToken, chocoToken]
        # tokens = [token]
        with ThreadPoolExecutor(max_workers=3) as executor:
            outStr = []
            for v in tokens:
                res = executor.submit(sendLineNotify, v, payload)
                outStr.append(res)

            for future in as_completed(outStr):
                if future.result().status_code == 200:
                    print('發送 LINE Notify 成功！')
                else:
                    print('發送 LINE Notify 失敗！')
        return
    except:
        return


THREE_TRADE = "https://tinyl.io/4fA1"
EGIHTGOV = "https://tinyl.io/4fA2"
ETF = "https://tinyl.io/4fA4"
FOREIGN = "https://tinyl.io/4fA6"


def stock5pm():
    msg = '\n 三大法人買賣超: %s \n\n 外資買賣超 %s \n\n八大官股: %s \n\n ETF溢價: %s' % (
        THREE_TRADE, FOREIGN, EGIHTGOV, ETF)
    payload = {'message': msg}
    res = sendLineNotify(token, payload)

    if res.status_code == 200:
        print('發送 LINE Notify 成功！')
    else:
        print('發送 LINE Notify 失敗！')


def punchMsgJob(name, url):
    return name+": "+tinyURL.makeTiny(url) + "\n\n"


def punchMsg(times, msgtext, rmin=0, rmax=10):
    """
    nowDate = datetime.date.today().strftime("%Y-%m-%d")
    randNum = random.randrange(rmin, rmax)
    Minsadded = datetime.timedelta(minutes=randNum)
    newTime = times + Minsadded

    urlKimi = "https://docs.google.com/forms/d/e/1FAIpQLSfKZAP0Ph2s3ATh3oYSmkxmMaUI64X0-dRL04SEfiQn4N9YOw/formResponse?entry.1343758667=蔡煜章&entry.1842948447=出勤刷卡&entry.529029656=%sT%s" % (
        nowDate, newTime.strftime("%H:%M"))

    # 重算時間
    randNum = random.randrange(11)
    Minsadded = datetime.timedelta(minutes=randNum)
    newTime = times + Minsadded
    urlCooper = "https://docs.google.com/forms/d/e/1FAIpQLSfKZAP0Ph2s3ATh3oYSmkxmMaUI64X0-dRL04SEfiQn4N9YOw/formResponse?entry.1343758667=趙榮聖&entry.1842948447=出勤刷卡&entry.529029656=%sT%s" % (
        nowDate, newTime.strftime("%H:%M"))

    urlDanny = "https://docs.google.com/forms/d/e/1FAIpQLSfKZAP0Ph2s3ATh3oYSmkxmMaUI64X0-dRL04SEfiQn4N9YOw/formResponse?entry.1343758667=李子川&entry.1842948447=出勤刷卡&entry.529029656=%sT%s" % (
        nowDate, times.strftime("%H:%M"))

    urls = {"Danny": urlDanny}

    msgArr = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        outStr = []
        for k, v in urls.items():
            res = executor.submit(punchMsgJob, k, v)
            outStr.append(res)
        for future in as_completed(outStr):
            msgArr.append(future.result())

    msg = '\n %s \n%s日記:%s ' % (
        msgtext, ''.join(msgArr), config('ETEN_DIARY', ""))
    """

    msg = '\n %s \n日記:%s ' % (
        msgtext, config('ETEN_DIARY', ""))

    return msg


def punchIn():
    time = datetime.datetime.now()
    defaultTime = time.replace(hour=8, minute=40)
    msg = punchMsg(defaultTime, "上班睡覺瞜~", 0, 5)
    payload = {'message': msg}
    res = sendLineNotify(etenToken, payload)

    if res.status_code == 200:
        print('發送 LINE Notify 成功！')
    else:
        print('發送 LINE Notify 失敗！')


def punchOut():
    time = datetime.datetime.now()
    defaultTime = time.replace(hour=17, minute=40)
    msg = punchMsg(defaultTime, "下班尿尿瞜~", 6, 10) + "\n\n"

    # 取得天氣資料
    loc = ["台北+內湖", "台北+大安", "新北+汐止", "新北+三重"]
    with ThreadPoolExecutor(max_workers=4) as executor:
        outStr = []
        for v in loc:
            res = executor.submit(getwttr, v)
            outStr.append(res)

        for future in as_completed(outStr):
            msg += future.result()+"\n"

    payload = {'message': msg}
    headers = {
        "Authorization": "Bearer " + etenToken,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    notify = requests.post(
        "https://notify-api.line.me/api/notify", headers=headers, params=payload)
    if notify.status_code == 200:
        print('發送 LINE Notify 成功！')
    else:
        print('發送 LINE Notify 失敗！')


def netflixMonList():
    url = "https://www.ptt.cc/bbs/EAseries/"
    regex = re.compile(r'.*Netflix台灣.*片單.*')
    pttRes = pttservice.getPTT(url, regex, "Netflix台灣")

    resMsg = ""
    if pttRes != "":
        resMsg = "%s\n%s\n%s\n" % (
            pttRes["Date"], pttRes["Title"], pttRes["Link"])

    nowMonth = datetime.datetime.today().month
    regex = re.compile(r'.*'+str(nowMonth)+'.*月.*')
    if regex.match(pttRes["Title"]) == None:
        return
    payload = {'message': resMsg}
    tokens = [netflixGrupToken, etenToken, carbeToken]
    with ThreadPoolExecutor(max_workers=2) as executor:
        outStr = []
        for v in tokens:
            res = executor.submit(sendLineNotify, v, payload)
            outStr.append(res)

        for future in as_completed(outStr):
            if future.result().status_code == 200:
                print('發送 LINE Notify 成功！')
            else:
                print('發送 LINE Notify 失敗！')
    return


def netflixMangFee():
    resMsg = " \n 目前管理費(一季) 390/4*3 = 292.5 \n 1/5, 4/5, 7/5, 10/5 收款 ^ ^ \n匯款給我 292  就好 ~~ \n\n Hi~麻煩轉帳至台新銀行(812)帳號是 %s 或是點擊連結開啟Richart APP可以直接帶入我的帳號唷 %s " % (bankAccount, bankAccountLink)
    payload = {'message': resMsg}
    res = sendLineNotify(netflixGrupToken, payload)
    if res.status_code == 200:
        print('發送 LINE Notify 成功！')
    else:
        print('發送 LINE Notify 失敗！')


def gasCPC():
    source = gasservice.getCPC()
    resMsg = ""
    if source != "":
        resMsg = "%s\t%s\n" % (
            source["Date"], source["Title"])
        for v in source["Data"]:
            resMsg += "%s : %s \n" % (v["name"], v["price"])

    payload = {'message': resMsg}
    tokens = [carbeToken, etenToken, chocoToken]

    with ThreadPoolExecutor(max_workers=2) as executor:
        outStr = []
        for v in tokens:
            res = executor.submit(sendLineNotify, v, payload)
            outStr.append(res)

        for future in as_completed(outStr):
            if future.result().status_code == 200:
                print('發送 LINE Notify 成功！')
            else:
                print('發送 LINE Notify 失敗！')
    return


def getDailyAWord(examp=True):
    resMsg = cambridgeservice.toMsg(cambridgeservice.getDailyAWord(), examp)
    payload = {'message': resMsg}
    tokens = [token]

    with ThreadPoolExecutor(max_workers=2) as executor:
        outStr = []
        for v in tokens:
            res = executor.submit(sendLineNotify, v, payload)
            outStr.append(res)

        for future in as_completed(outStr):
            if future.result().status_code == 200:
                print('發送 LINE Notify 成功！')
            else:
                print('發送 LINE Notify 失敗！')
    return


def getInvoice(msg="發票"):
    resMsg = invoiceservice.getInvoice(msg)
    print(resMsg)
    payload = {'message': resMsg}
    tokens = [carbeToken, etenToken, chocoToken]

    with ThreadPoolExecutor(max_workers=2) as executor:
        outStr = []
        for v in tokens:
            res = executor.submit(sendLineNotify, v, payload)
            outStr.append(res)

        for future in as_completed(outStr):
            if future.result().status_code == 200:
                print('發送 LINE Notify 成功！')
            else:
                print('發送 LINE Notify 失敗！')
    return


def threeDayWether(loc="新北+汐止"):
    try:
        url = "https://zh-tw.wttr.in/%s%s" % (loc, ".png")
        res = requests.get(url, headers=headers, stream=True)
        payload = {'message': loc}

        # 寫入檔案
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        # res.raw.decode_content = True
        # # Open a local file with wb ( write binary ) permission.
        # with open("New-Taipei.png", 'wb') as f:
        #     shutil.copyfileobj(res.raw, f)
        # f = open('New-Taipei.png', 'rb')  # create an empty demo file
        # file = {'imageFile': f}
        file = {'imageFile': res.raw}

      # tokens = [carbeToken, etenToken, chocoToken]
        tokens = [token]
        with ThreadPoolExecutor(max_workers=3) as executor:
            outStr = []
            for v in tokens:
                res = executor.submit(sendLineNotify, v, payload, file)
                outStr.append(res)

            for future in as_completed(outStr):
                if future.result().status_code == 200:
                    print('發送 LINE Notify 成功！')
                else:
                    print('發送 LINE Notify 失敗！')
        return
    except Exception as e:
        print(e)
        return


def getwttr(loc):
    url = "https://zh-tw.wttr.in/%s?m&format=%s&lang=%s" % (
        loc, '%l:+%c+%C+%t', "zh-tw")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
        'Accept-Language': "zh-tw"
    }
    res = requests.get(url, headers=headers)
    return res.text


def wether(title=None, loc=[]):
    try:
        msg = ""
        # 取得天氣資料
        with ThreadPoolExecutor(max_workers=4) as executor:
            outStr = []
            for v in loc:
                res = executor.submit(getwttr, v)
                outStr.append(res)

            for future in as_completed(outStr):
                msg += future.result()+"\n"
        payload = {'message': title+"\n"+msg}

        # tokens = [token]
        tokens = [etenToken]

        # 發送line
        with ThreadPoolExecutor(max_workers=3) as executor:
            outStr = []
            for v in tokens:
                res = executor.submit(sendLineNotify, v, payload)
                outStr.append(res)

            for future in as_completed(outStr):
                if future.result().status_code == 200:
                    print('發送 LINE Notify 成功！')
                else:
                    print('發送 LINE Notify 失敗！')
        return
    except Exception as e:
        print(e)
        return


if __name__ == "__main__":
    # stock5pm()
    # punchIn()
    # punchOut()
    # test()
    # covid19()
    # netflixMonList()
    # netflixMangFee()
    # gasCPC()
    # getDailyAWord()
    # carbe()
    # threeDayWether()
    # lunch("Taipei+Neihu", "New-Taipei+Xizhi")
    # wether(title="放飯了~", loc=["台北+內湖", "台北+大安", "新北+汐止", "新北+三重"])
    # getInvoice()
    # star()
    starDay()
