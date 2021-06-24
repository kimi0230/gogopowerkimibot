from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from django.conf import settings
from decouple import config
from utility import tinyURL
import re
from services import pttservice

import datetime
from services import covid19service

import random
try:
    token = settings.ZHIZHI_NOTIFY_TOKEN
except:
    # for local test
    token = config('ZHIZHI_NOTIFY_TOKEN')

carbeToken = config('CARBE_NOTIFY_TOKEN')
try:
    etenToken = settings.ETEN_NOTIFY_TOKEN
except:
    etenToken = config('ETEN_NOTIFY_TOKEN')

chocoToken = config('CHOCO_NOTIFY_TOKEN')
netflixGrupToken = config('NETFLIXGRUP_NOTIFY_TOKEN')


def test():
    msg = '起床尿尿摟'
    payload = {'message': msg}
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    notify = requests.post(
        "https://notify-api.line.me/api/notify", headers=headers, params=payload)
    if notify.status_code == 200:
        print('發送 LINE Notify 成功！')
    else:
        print('發送 LINE Notify 失敗！')


def carbe():
    msg = '卡比起床尿尿'
    payload = {'message': msg}
    headers = {
        "Authorization": "Bearer " + carbeToken,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    notify = requests.post(
        "https://notify-api.line.me/api/notify", headers=headers, params=payload)
    if notify.status_code == 200:
        print('發送 LINE Notify 成功！')
    else:
        print('發送 LINE Notify 失敗！')


def sendLineNotify(token, params):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    notify = requests.post(
        "https://notify-api.line.me/api/notify", headers=headers, params=params)
    return notify


def covid19():
    pttRes = covid19service.getGossipCovid19()
    resMsg = ""
    if pttRes != "":
        resMsg = "%s\n%s\n%s\n" % (
            pttRes["Date"], pttRes["Title"], pttRes["Link"])
    payload = {'message': resMsg}

    tokens = [carbeToken, etenToken, chocoToken]
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


THREE_TRADE = "https://www.twse.com.tw/zh/page/trading/fund/BFI82U.html"
EGIHTGOV = "https://histock.tw/stock/broker8.aspx"
ETF = "https://mis.twse.com.tw/stock/etf_nav.jsp?ex=tse#memo3"


def stock5pm():
    msg = '\n 三大法人買賣超: %s \n\n 八大官股: %s \n\n ETF溢價: %s' % (
        THREE_TRADE, EGIHTGOV, ETF)
    payload = {'message': msg}
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    notify = requests.post(
        "https://notify-api.line.me/api/notify", headers=headers, params=payload)
    if notify.status_code == 200:
        print('發送 LINE Notify 成功！')
    else:
        print('發送 LINE Notify 失敗！')


def punchMsgJob(name, url):
    return name+": "+tinyURL.makeTiny(url) + "\n\n"


def punchMsg(times, msgtext, rmin=0, rmax=10):
    nowDate = datetime.date.today().strftime("%Y-%m-%d")
    randNum = random.randrange(rmin, rmax)
    Minsadded = datetime.timedelta(minutes=randNum)
    newTime = times + Minsadded

    urlKimi = "https://docs.google.com/forms/d/e/1FAIpQLSfKZAP0Ph2s3ATh3oYSmkxmMaUI64X0-dRL04SEfiQn4N9YOw/formResponse?entry.1343758667=蔡煜章&entry.1842948447=出勤刷卡&entry.529029656=%sT%s" % (
        nowDate, newTime.strftime("%H:%M"))
    # urlKimi = tinyURL.makeTiny(urlKimi)

    # 重算時間
    randNum = random.randrange(11)
    Minsadded = datetime.timedelta(minutes=randNum)
    newTime = times + Minsadded
    urlCooper = "https://docs.google.com/forms/d/e/1FAIpQLSfKZAP0Ph2s3ATh3oYSmkxmMaUI64X0-dRL04SEfiQn4N9YOw/formResponse?entry.1343758667=趙榮聖&entry.1842948447=出勤刷卡&entry.529029656=%sT%s" % (
        nowDate, newTime.strftime("%H:%M"))
    # urlCooper = tinyURL.makeTiny(urlCooper)

    urlDanny = "https://docs.google.com/forms/d/e/1FAIpQLSfKZAP0Ph2s3ATh3oYSmkxmMaUI64X0-dRL04SEfiQn4N9YOw/formResponse?entry.1343758667=李子川&entry.1842948447=出勤刷卡&entry.529029656=%sT%s" % (
        nowDate, times.strftime("%H:%M"))
    # urlDanny = tinyURL.makeTiny(urlDanny)

    urls = {"Kimi": urlKimi, "Cooper": urlCooper, "Danny": urlDanny}

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

    return msg


def punchIn():
    time = datetime.datetime.now()
    defaultTime = time.replace(hour=8, minute=40)
    msg = punchMsg(defaultTime, "上班睡覺瞜~", 0, 5)
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


def punchOut():
    time = datetime.datetime.now()
    defaultTime = time.replace(hour=17, minute=40)
    msg = punchMsg(defaultTime, "下班尿尿瞜~", 6, 10)
    print(msg)
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


if __name__ == "__main__":
    # stock5pm()
    # punchIn()
    # punchOut()
    # test()
    # covid19()
    netflixMonList()
