from typing import Text
import requests
from bs4 import BeautifulSoup
import locale

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}

link = "https://www.taiwanlottery.com.tw/index_new.aspx"


def getlottery():
    try:
        res = requests.get(link, headers=headers)
        if res.status_code != 200:
            return
        soup = BeautifulSoup(res.text, "lxml")
        # print(soup)
        # super lotto
        # big lotto

        def extractionlotto(item, counts):
            time = item.select("span.font_black15")[0].text.strip()
            numbers = [] if len(item.select(
                ".ball_tx")) == 0 else[ball.text for ball in item.select(".ball_tx")]
            specialNumber = 0 if len(item.select(
                "div.ball_red")) == 0 else item.select("div.ball_red")[0].text
            outputOrder = ", ".join(numbers[:6])
            ascOrder = ", ".join(numbers[counts:])
            return {"time": time, "outputOrder": outputOrder, "ascOrder": ascOrder, "specialNumber": specialNumber, }

        # 威力彩, 38樂合彩, 大樂透, 49樂合彩, 六組數字, 抓出威力彩跟大樂透
        titles = ["威力彩", "38樂合彩", "大樂透", "49樂合彩"]
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        topDollar = [] if len(soup.select(".top_dollar")) == 0 else [
            locale.currency(int(dollar.text), grouping=True) for dollar in soup.select(".top_dollar")]
        lottos = {} if len(soup.select(".contents_box02")) == 0 else {
            titles[idx]: extractionlotto(box, 6) for idx, box in enumerate(soup.select(".contents_box02")) if idx % 2 == 0}
        lottos["威力彩"]["topDollar"] = topDollar[0].split(".")[0]
        lottos["大樂透"]["topDollar"] = topDollar[1].split(".")[0]
        return lottos
    except Exception as e:
        print(e)
        return ""


def getlotteryText(category=["威力彩", "大樂透"]):
    lotterys = getlottery()
    msg = ""

    for title in category:
        msg += genLineMsg(title, lotterys[title])

    lotteryShortURL = "\n\nhttps://tinyl.io/4lb9"
    return msg.strip() + lotteryShortURL


def genLineMsg(title, lottery):
    msg = "%s\n%s\n大小順序: %s\n特別號: %s\n頭獎: %s\n\n\n" % (title,
                                                       lottery["time"], lottery["ascOrder"], lottery["specialNumber"], lottery["topDollar"])
    return msg


if __name__ == "__main__":
    # python3 -B -m services.taiwanlotteryservice
    # print(getlottery())
    print(getlotteryText())
