# 匯入庫
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from io import StringIO
import locale
import ssl

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}
ssl._create_default_https_context = ssl._create_unverified_context

plt.rcParams["font.sans-serif"] = [u'Arial Unicode MS']  # 設定中文字型
plt.rcParams["axes.unicode_minus"] = False
pd.options.mode.chained_assignment = None  # 取消顯示pandas資料重設警告
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def printTable(dfs):
    table = ("{:<30} {:<20} {:<20} {:<20} \n".format(" ", *dfs.columns.values))
    indexTitle = dfs.index.values
    for idx, v in enumerate(dfs.values):
        table += ("{:15} {:^20} {:^20} {:^20}\n".format(
            indexTitle[idx], *[locale.currency(int(c), grouping=True)[:-3] for c in v]))
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
            "title": title,
            "data": printTable(dfs)
        }
        return result

        # plt.figure(figsize=(10, 5))
        # ax = plt.axes(frame_on=False)  # 不要額外框線
        # ax.set_title("三大法人買賣超")
        # ax.xaxis.set_visible(False)  # 隱藏X軸刻度線
        # ax.yaxis.set_visible(False)  # 隱藏Y軸刻度線
        # ax.axis('off')
        # pd.plotting.table(ax, dfs, loc='center', colWidths=[0.1] * 3)
        # plt.savefig('table.png', dpi=200, bbox_inches='tight')     # 存檔
        # plt.show()
        # f = open('table.png', 'rb')  # create an empty demo file
        # file = {'imageFile': f}
        # headers = {
        #     "Authorization": "Bearer " + "msgG1hovWso1zkinUPL0335RVNV1h5TTzET9F1W92Q6",
        #     # "Content-Type": "application/x-www-form-urlencoded"
        # }
        # params = {'message': "ddd"}
        # notify = requests.post(
        #     "https://notify-api.line.me/api/notify", headers=headers, params=params, files=file)
        # return notify

    except Exception as e:
        print(e)
        return ""


def test():
    try:
        url = "https://www.twse.com.tw/zh/page/trading/fund/BFI82U.html"
        res = requests.get(url, headers=headers)

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


if __name__ == "__main__":
    print(getThreeRrade())

    # f = open('table.png', 'rb')  # create an empty demo file
    # file = {'imageFile': f}
    # payload = {'message': "121212"}
