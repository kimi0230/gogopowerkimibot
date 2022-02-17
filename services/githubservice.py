
import requests
from bs4 import BeautifulSoup


default_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
}


def getKimi0230():
    try:
        # url = "https://visitor-badge.glitch.me/badge?page_id=kimi0230"
        url = "https://steel-quark-crabapple.glitch.me/badge?page_id=kimi0230"
        res = requests.get(url, headers=default_headers, verify=False)
        res.encoding = 'UTF-8'
        soup = BeautifulSoup(res.text, "lxml")
        vistorCount = soup.select("text")[-1].text
        return vistorCount
    except:
        return None


if __name__ == "__main__":
    print(getKimi0230())
