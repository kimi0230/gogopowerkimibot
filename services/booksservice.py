import requests
from django.conf import settings

GET_REOCRDER = "https://myaccount.books.com.tw/myaccount/myaccount/getReorder"
CHECKIN_URL = "https://myaccount.books.com.tw/myaccount/reader/dailySignIn/?ru=P5zqo53d"

default_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
}

default_cookies = settings.BOOKS_COOKIES


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
