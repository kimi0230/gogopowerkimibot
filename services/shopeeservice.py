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
            LUCKY_URL, headers=default_headers, cookies={"Cookie": mycookies}, json=bodyJson)

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

        testCookies = {'Cookie': 'REC_T_ID=8e0ac738-403e-11ec-bc85-b47af14b1498; SPC_F=oZWe4xEBFSeml3DnKJ87FdNOCR7vq5LS; csrftoken=CHwquLl5W8L3izN007no6DyfnwrEwvqo; SPC_IA=-1; welcomePkgShown=true; _QPWSDCXHZQA=ac71af35-6b35-4013-db2e-884ed63a6497; G_ENABLED_IDPS=google; SPC_CLIENTID=b1pXZTR4RUJGU2Vthrdudfduuxitkrqq; spc_ckt_reqid=1f8a1b84d6f2f01802ef8382869cfa00:010001ed435577f3:0000008a82ab8eb3; __LOCALE__null=TW; SC_DFP=hbYLpsPhIKsRmDlNOVyambFqjLz2EETZ; __stripe_mid=e07c712c-2add-40bf-90fa-d63aa93314a525023a; SPC_T_ID="e+bCTowwo2HaRJ6Rix+HQbvYu8ZHic6ZiwhWR+0Zlc6VU704Gz7aMdUOZHRpSeN3Bfo2pxcwnZsQW50kg1pFZi66ouB24llWppMIZrwMSeU="; SPC_T_IV="XBUWWjKZckMDuu3ndoUtLw=="; SPC_SI=vhVRYwAAAAB6V25PcE11axAzRgAAAAAAVlVnTlVwd3Y=; SPC_ST=.a2tlYTVnT0lOcjRhSkZFVjhsUDGgD36gcg+x92YKZTr7wIfIBohrv2xum/oLu9Ml60D2FU9UzMRdTVA6bVtFbuZwYM3azl7eekb2m7O7jns7yfYNg9hen5529RyiLvcuukKh7ugX++YoR4+YWnSL+XW3H/1HLpVN/Zr+WHqPMmtZ3dERmHq62W6fgs7Cewh4Qp9xDdKgKlvGsakfLX6V1g==; SPC_U=37913853; SPC_T_IV=REIxdGMzMmVYdXZSOGZVaw==; SPC_R_T_ID=3wLopXFPRE9YYR4DNu31lF2KQcsfANsccmbjJ/UETM/uALFUY+fZorfJwnFE9Bi3zylaj2pOQ7peIee8BYyTiGRul3YM9mOt7MzMADrRGHFUEpjSKF+NDn0SSqJDIU+ViMjgfUJh/w4qDR9r2XZIq/LVNbNo6koQBTUGu65baRk=; SPC_R_T_IV=REIxdGMzMmVYdXZSOGZVaw==; SPC_T_ID=3wLopXFPRE9YYR4DNu31lF2KQcsfANsccmbjJ/UETM/uALFUY+fZorfJwnFE9Bi3zylaj2pOQ7peIee8BYyTiGRul3YM9mOt7MzMADrRGHFUEpjSKF+NDn0SSqJDIU+ViMjgfUJh/w4qDR9r2XZIq/LVNbNo6koQBTUGu65baRk=; shopee_webUnique_ccd=DYxmzcle60wrtZxg8INDmA==|LX1pmt95GfErpOR/ONEMOGJ+9MJYzHYJRSwB7jzItwx3/Uz0ViExoyA+eiETFLoiQDj3WSCSU9RjVywULggc4kKUnoXa4dKB2DeT|8Bo6PMkCprzpMOLw|06|3; ds=6ab8e99cd89385cfd084e76936e5d8f7; SPC_EC=OFZ5QWlGZ2pZemRxZ3dMRJwjweVBmTY48G9sAKe0hhOnOKUDKQs7dZuwyOTNu9CrRW7rTz4AImRBabXjqfrejXRN9NRx2vwWip2TD2OegT+ZJaRezp62oBIDvIV1IvT0hyq1yA+4tE9ChBTDWbLUfLhjacd/OfSmUqybB0yv9NA='}
        res = requests.post(
            CHECKIN_URL, headers=default_headers, cookies=testCookies)
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
