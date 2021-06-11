import requests

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

url = 'http://invoice.etax.nat.gov.tw/invoice.xml'


def getInvoice(msg):
    try:
        number = [int(num) for num in msg.split() if num.isdigit()]
        if len(number) > 0:
            index = number[0]
        else:
            index = 0

        content = requests.get(url)
        tree = et.fromstring(content.text)  # 解析XML
        link = tree.find('channel')[1].text.replace('http', 'https')
        items = list(tree.iter(tag='item'))  # 取得item標籤內容
        title = items[index][0].text  # 期別
        ptext = items[index][2].text  # 中獎號碼
        ptext = ptext.replace('<p>', '').replace('</p>', '\n')
        message = link + '\n' + title + '月\n' + \
            ptext[:-1]  # ptext[:-1]為移除最後一個\n
        return message
    except:
        return ""


if __name__ == "__main__":
    print(getInvoice("發票"))
