import urllib.request
import datetime
from decouple import config


def wakeup():
    url = config('APP_URL', default='APP_URL')
    conn = urllib.request.urlopen(url)
    print("wakeup at : ", datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
    for key, value in conn.getheaders():
        print(key, value)


if __name__ == "__main__":
    wakeup()
