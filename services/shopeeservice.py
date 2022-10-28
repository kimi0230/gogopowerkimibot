from http import cookies
import requests
import random
import ast
from django_redis import get_redis_connection
from utility import redisUtility

CHECKIN_URL = "https://shopee.tw/mkt/coins/api/v2/checkin"
LOGIN_URL = "https://shopee.tw/api/v4/account/login_by_password"
LUCKY_URL = "https://games.shopee.tw/luckydraw/api/v1/lucky/event/0244d69e637bbb73"

default_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
    'Content-Type': 'application/json'
}


def getLucky(email="", password=""):
    try:
        r = get_redis_connection("heroku")
        redisKey = "Cookies:shopee:"+email
        if r.exists(redisKey):
            mycookies = r.get(redisKey)
            mycookies = mycookies.decode("UTF-8")
        else:
            mycookies = getCookies(email, password)
            redisUtility.acquireLock(r, redisKey, mycookies, 60*60*12*7)

        requestID = ("%.0f" % (random.random() * 10**20))[:16]
        bodyJson = {
            "request_id": requestID,
            "app_id": "E9VFyxwmtgjnCR8uhL",
            "activity_code": "010ac47631cf4bb5",
            "source": 0
        }
        res = requests.post(
            LUCKY_URL, headers=default_headers, cookies={"Cookie": "'"+mycookies+"'"}, json=bodyJson)

        if res.status_code != 200:
            return None
        return res.json()
    except Exception as e:
        print(e)
        return None


def checkin(email="", password=""):
    try:
        r = get_redis_connection("heroku")
        redisKey = "Cookies:shopee:"+email
        if r.exists(redisKey):
            mycookies = r.get(redisKey)
            mycookies = mycookies.decode("UTF-8")
            print("-------redddd--->", mycookies)
        else:
            mycookies = getCookies(email, password)
            redisUtility.acquireLock(r, redisKey, mycookies, 60*60*12*7)
            print("-------reqqq--->", mycookies)

        res = requests.post(
            CHECKIN_URL, headers=default_headers, cookies={"Cookie": "'"+mycookies+"'"})
        print("------------------>", res.json())
        if res.status_code != 200:
            return None
        return res.json()
    except Exception as e:
        print(e)
        return None


def getCookies(email="", password=""):
    try:
        payload = {
            "email": email,
            "password": password,
            "support_ivs": True
        }
        retry = 3
        for i in range(0, retry):
            res = requests.post(
                LOGIN_URL, headers=default_headers, json=payload)
            if i == retry-1 and res.status_code != 200:
                print("retry 3 times")
                return None
            if res.status_code != 200:
                continue
            else:
                break

        # https://stackoverflow.com/questions/19926089/python-equivalent-of-java-stringbuffer
        cookeis = ''.join(
            [val+"="+res.cookies[val]+';' for val in res.cookies.keys()])

        return cookeis[:-1]
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    c = 'Sc'
    print(checkin("", ""))
    # print(getLucky())
    # print(getCookies())
