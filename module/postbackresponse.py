
from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage
import datetime

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def sendBack_buy(event, backdata):  # 處理Postback
    try:
        text1 = '感謝您購買披薩，我們將盡快為您製作。\n(action 的值為 ' + \
            backdata.get('action') + ')'
        text1 += '\n(可將處理程式寫在此處。)'
        message = TextSendMessage(  # 傳送文字
            text=text1
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendBack_sell(event, backdata):  # 處理Postback
    try:
        message = TextSendMessage(  # 傳送文字
            text='點選的是賣 ' + backdata.get('item')
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendDate_sell(event, backdata):  # Postback,顯示日期時間
    try:
        if backdata.get('mode') == 'date':
            dt = '日期為：' + event.postback.params.get('date')  # 讀取日期
        elif backdata.get('mode') == 'time':
            dt = '時間為：' + event.postback.params.get('time')  # 讀取時間
        elif backdata.get('mode') == 'datetime':
            dt = datetime.datetime.strptime(event.postback.params.get(
                'datetime'), '%Y-%m-%dT%H:%M')  # 讀取日期時間
            dt = dt.strftime(
                '{d}%Y-%m-%d, {t}%H:%M').format(d='日期為：', t='時間為：')  # 轉為字串
        message = TextSendMessage(
            text=dt
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！'))
