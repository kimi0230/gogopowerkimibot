# 匯入庫
import re
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import ssl
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from utility import tinyURL
from services import mailservice
from email.mime.text import MIMEText
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}
ssl._create_default_https_context = ssl._create_unverified_context

plt.rcParams["font.sans-serif"] = [u'Arial Unicode MS']  # 設定中文字型
plt.rcParams["axes.unicode_minus"] = False
pd.options.mode.chained_assignment = None  # 取消顯示pandas資料重設警告
# locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def printThreeRradeTable(dfs):
    table = ""
    indexTitle = dfs.index.values
    for idx, v in enumerate(dfs.values):
        table += "## %s\n(買) %s\t(賣) %s\n(差) %s\n\n" % (indexTitle[idx], *[
            round(float(c)/float(100000000), 2) for c in v])
    return table


def getThreeRrade():
    # 三大法人
    try:
        url = "https://www.twse.com.tw/fund/BFI82U?response=html&dayDate=&weekDate=&monthDate=&type=day"
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "lxml")
        title = soup.select("th>div")[0].text

        dfs = pd.read_html(
            url, header=1, keep_default_na=False, index_col=0)[0]

        result = {
            "title": title+"(億)",
            "data": printThreeRradeTable(dfs),
            "url": "https://tinyl.io/5PL9"
        }
        return result

    except Exception as e:
        print(e)
        return None


def printForeignTable(dfs, tops=11):
    buyRank = "買超\n股票\t超張數\t漲跌\n"
    sellRank = "賣超\n股票\t超張數\t漲跌\n"
    # ['股票名稱' '超張數' '收盤價' '漲跌' '名次' '股票名稱' '超張數' '收盤價' '漲跌']
    for idx, v in enumerate(dfs.values[1:tops]):
        buyRank += ("({}) {}: {}元\n {:^7},\t{}\n").format(idx +
                                                          1, v[0], v[2], v[1], v[3])
        sellRank += ("({}) {}: {}元\n {:^7},\t{}\n").format(idx +
                                                           1, v[5], v[7], v[6], v[8])

    return "%s\n%s" % (buyRank, sellRank)


def getForeign(tops=10):
    try:
        url = "https://fubon-ebrokerdj.fbs.com.tw/Z/ZG/ZGK_D.djhtm"
        res = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(res.text, "lxml")
        title = soup.select("div.t11")[0].text + "\t外資買賣超"
        dfs = pd.read_html(
            url, header=1, keep_default_na=False, index_col=0)[1]

        result = {
            "title": title,
            # +1 因為開頭有['股票名稱' '超張數' '收盤價' '漲跌' '名次' '股票名稱' '超張數' '收盤價' '漲跌']欄位
            "data": printForeignTable(dfs, tops+1),
            "url": "https://tinyl.io/5PND"
        }
        return result
    except Exception as e:
        print(e)
        return None


def test():
    try:
        url = "https://www.twse.com.tw/zh/page/trading/fund/BFI82U.html"

        # 用Numpy建立樣本
        table = np.random.rand(10, 5)
        table = np.round(table, 2)

        # 用Pandas將樣本轉成DataFrame
        table_pd = pd.DataFrame(table)
        table_pd.columns = ['A', 'B', 'C', 'D', 'E']
        table_pd.index = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

        # DataFrame=>png
        plt.figure('123')            # 視窗名稱
        ax = plt.axes(frame_on=False)  # 不要額外框線
        ax.xaxis.set_visible(False)  # 隱藏X軸刻度線
        ax.yaxis.set_visible(False)  # 隱藏Y軸刻度線
        # 將mytable投射到ax上，且放置於ax的中間
        pd.plotting.table(ax, table_pd, loc='center')
        k = plt.savefig('table.png')     # 存檔
    except:
        return ""


def k():
    mtext = "外資 1"
    if re.match(r"^外資\s?\d{0,2}", mtext) != None:
        nums = re.sub(r'\D', "", mtext)
        if nums == "":
            nums = 5
        res = getForeign(int(nums))
        print(res)
    else:
        print("kkk")


sinotrade = "https://www.sinotrade.com.tw/richclub/weeklyreport"


def getWeekEvent():
    try:
        # 永豐用GrapqhQL

        transport = RequestsHTTPTransport(
            url="https://www.sinotrade.com.tw/richclub/api/graphql",
            verify=True, retries=3,
        )

        # Create a GraphQL client using the defined transport
        client = Client(transport=transport,
                        fetch_schema_from_transport=False)

        # Provide a GraphQL query
        query = gql(
            """
            query ($input: clientGetContentListInput) {
                clientGetArticleList(input: $input) {
                    total
                    filtered {
                    _id
                    createdAt
                    pubDate
                    title
                    updatedAt
                    author {
                        _id
                        name {
                        CN
                        account
                        __typename
                        }
                        __typename
                    }
                    channel {
                        _id
                        name {
                        CN
                        account
                        __typename
                        }
                        __typename
                    }
                    stock {
                        code
                        name
                        __typename
                    }
                    image
                    __typename
                    }
                    __typename
                }
            }
            """
        )

        params = {
            "input": {
                "page": 0,
                "limit": 10,
                "channel": "5ea796f104ce153684fa1b04"
            }
        }
        # Execute the query on the transport
        queryResult = client.execute(query, variable_values=params)
        title = queryResult["clientGetArticleList"]["filtered"][0]["title"]
        link = tinyURL.makeTiny(("{}{}-{}").format("https://www.sinotrade.com.tw/richclub/weeklyreport/",
                                                   re.sub('\W', '-', title), queryResult["clientGetArticleList"]["filtered"][0]["_id"]))
        date = queryResult["clientGetArticleList"]["filtered"][0]["updatedAt"]
        result = {
            "title": title,
            "data": link,
            "images": [],
            "url": link,
            "date": datetime.fromtimestamp(int(date)/1000).strftime('%Y-%m-%d %H:%M:%S')
        }
        return result

    except Exception as e:
        print(e)
        return None

# 永豐理財行事曆


def Calendar(event):
    # A=0&B=&C=0, A事件 B 起始日期(2022-4-23) C 上下兩週(-2/0/2)
    # 事件 A
    #  "0"         所有
    #  "EV000100"  上櫃轉上市掛牌
    #  "EV000130"  交易所類股調整
    #  "EV000060"  法人說明會
    #  "EV000010"  股東會
    #  "EV000011"  股東臨時會
    #  "EV000050"  重大訊息
    #  "EV000170"  海外法人說明會
    #  "EV000160"  特別股掛牌
    #  "EV000080"  記者會
    #  "EV000020"  除權息
    #  "EV000110"  終止掛牌
    #  "EV000120"  減資後新股掛牌
    #  "EV000090"  新股掛牌
    #  "EV000140"  新產品發表會
    #  "EV000070"  業績發表會
    #  "EV000150"  增資股上市
    #  "EV000101"  興櫃掛牌
    b = ""
    c = "0"
    # 玉山
    # url = "https://sjmain.esunsec.com.tw/z/ze/zej/zej.djhtm?A=%s&B=%s&C=%s" % (event, b, c)
    # 永豐
    url = "https://stockchannelnew.sinotrade.com.tw/z/ze/zej/zej.djhtm?A=%s&B=%s&C=%s" % (
        event, b, c)
    print("url = ", url)
    dfs = pd.read_html(url)

    # 讓email 發中文 https://books.bod.idv.tw/2019/07/pythongmailsmtputf8-base64.html
    body = MIMEText("<h1>"+url+"</h1><br><br>" +
                    dfs[3].to_html(), 'html', 'utf-8')
    mailservice.SendMail("kimi0230@gmail.com", "kk",
                         body)


if __name__ == "__main__":
    # weekEvent()
    # print(getThreeRrade())
    # getForeign()
    # f = open('table.png', 'rb')  # create an empty demo file
    # file = {'imageFile': f}
    # payload = {'message': "121212"}
    Calendar("EV000020")
