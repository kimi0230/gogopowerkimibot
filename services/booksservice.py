import requests

GET_REOCRDER = "https://myaccount.books.com.tw/myaccount/myaccount/getReorder"
CHECKIN_URL = "https://myaccount.books.com.tw/myaccount/reader/dailySignIn/?ru=P5zqo53d"

default_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
}

default_cookies = {
    "Cookie": "bid=618b235c684f2; item_history=F014084384+; ssid=618b235c684f2.1639372812; bt=r41g5o; lpk=dc2d5afdeb0b093dbd52498395398104b438e1c4e7b64a6081a271edb8ded5ff5e414c3499410886; cid=sherlock8; bday=1989/02/01; pd=B4sJqHxLBW3.UO9EP7BnKgErGY; gud=4780f2b43e12a7e68c202bb28a4259f9712d86348704730e6590213d7d5a27290477d4193ab2025720eb817159d71662f7bc1473a6cf7fc677c788f9b1703749; bid=61b6d813cc5e7"
}


def updatelpkUrl(cookies=default_cookies):
    try:
        res = requests.get(
            GET_REOCRDER, headers=default_headers, cookies=cookies)
        if res.status_code == 200:
            print(res.cookies)
            print(res.text)

        else:
            print("連線錯誤‼️")
            return None
    except Exception as e:
        print(e)
        return None


def checkin(cookies=default_cookies):
    try:
        res = requests.post(
            CHECKIN_URL, headers=default_headers, cookies=cookies)
        return res.json()
    except Exception as e:
        print(e)
        return None


if __name__ == "__main__":
    print(checkin())
