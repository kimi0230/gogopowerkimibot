import requests
from django.conf import settings
from decouple import config

try:
    token = settings.ZHIZHI_NOTIFY_TOKEN
except:
    # for local test
    token = config('ZHIZHI_NOTIFY_TOKEN')

carbeToken = config('CARBE_NOTIFY_TOKEN')


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


if __name__ == "__main__":
    stock5pm()
