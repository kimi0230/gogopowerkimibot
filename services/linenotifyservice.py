from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from django.conf import settings
from decouple import config
from utility import tinyURL
import datetime

import random
try:
    token = settings.ZHIZHI_NOTIFY_TOKEN
except:
    # for local test
    token = config('ZHIZHI_NOTIFY_TOKEN')

carbeToken = config('CARBE_NOTIFY_TOKEN')

etenToken = config('ETEN_NOTIFY_TOKEN')


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

    urls = [urlKimi, urlCooper, urlDanny]
    msg = '\n %s \n'
    with ThreadPoolExecutor(max_workers=3) as executor:
        outStr = []
        for n in urls:
            res = executor.submit(punchMsgJob, n)
            outStr.append(res)

    msg += ''.join(outStr)+"日記: "+config('ETEN_DIARY', "")

    # msg = '\n %s \n Kimi: %s \n\n Cooper: %s \n\n Danny: %s \n\n 日記: %s ' % (
    #     msgtext, urlKimi, urlCooper, urlDanny, config('ETEN_DIARY', ""))
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


if __name__ == "__main__":
    # stock5pm()
    # punchIn()
    punchOut()
