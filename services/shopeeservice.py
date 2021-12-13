import requests
import random

CHECKIN_URL = "https://shopee.tw/mkt/coins/api/v2/checkin"
LUCKY_URL = "https://games.shopee.tw/luckydraw/api/v1/lucky/event/0244d69e637bbb73"

default_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
}


def getLucky(cookies):
    try:
        requestID = ("%.0f" % (random.random() * 10**20))[:16]
        body = {
            "request_id": requestID,
            "app_id": "E9VFyxwmtgjnCR8uhL",
            "activity_code": "010ac47631cf4bb5",
            "source": 0
        }
        res = requests.post(
            LUCKY_URL, headers=default_headers, cookies=cookies, data=body)
        if res.status_code != 200:
            return None
        return res.json()
    except Exception as e:
        print(e)
        return None


def checkin(cookies):
    try:
        # print(cookies)
        res = requests.post(
            CHECKIN_URL, headers=default_headers, cookies=cookies)
        if res.status_code != 200:
            return None
        return res.json()
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    c = ''
    # print(checkin({"Cookie": c}))
    print(getLucky({"Cookie": c}))
