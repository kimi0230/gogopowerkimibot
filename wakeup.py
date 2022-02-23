import urllib.request


def wakeup():
    url = "https://xxx.com"
    conn = urllib.request.urlopen(url)

    for key, value in conn.getheaders():
        print(key, value)


if __name__ == "__main__":
    wakeup()
