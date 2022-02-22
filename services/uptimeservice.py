
import requests


def check(url):
    try:
        res = requests.get(url)
        # print(res.json())
        print('%s \t %s' % (url, res))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    check("https://steel-quark-crabapple.glitch.me/kimi")
