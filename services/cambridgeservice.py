import requests
import re
from bs4 import BeautifulSoup

# fix: InsecureRequestWarning: Unverified HTTPS request is being made to host
import requests.packages.urllib3

url = "https://dictionary.cambridge.org/zht"


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}


def getDayWord():
    res = requests.get(url, headers=headers)
    res.encoding = 'UTF-8'
    soup = BeautifulSoup(res.text, "lxml")
    word = soup.select(".fs36.lmt-5.feature-w-big.wotd-hw a")[0].text
    print(word)

    wordURL = 'https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/'+word
    print(wordURL)


if __name__ == "__main__":
    print(getDayWord())
