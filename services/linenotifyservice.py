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
    print("kimimimimimimimimii")
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


if __name__ == "__main__":
    test()
