
from django.conf import settings

from linebot import LineBotApi
from linebot.models import BaseSize, TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn, DatetimePickerTemplateAction, ImagemapSendMessage, MessageImagemapAction, ImagemapArea, URIImagemapAction
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def sendButton(event):  # 按鈕樣版
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',  # 顯示的圖片
                title='按鈕樣版示範',  # 主標題
                text='請選擇：',  # 副標題
                actions=[  # 最多四個
                    MessageTemplateAction(  # 顯示文字計息
                        label='文字訊息',
                        text='@購買披薩'
                    ),
                    URITemplateAction(  # 開啟網頁
                        label='連結網頁',
                        uri='https://github.com/kimi0230/linebot_practise'
                    ),
                    PostbackTemplateAction(  # 執行Postback功能,觸發Postback事件
                        label='回傳訊息',  # 按鈕文字
                        # text='@購買披薩',  #顯示文字計息
                        data='action=buy'  # Postback資料
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendConfirm(event):  # 確認樣板
    try:
        message = TemplateSendMessage(
            alt_text='確認樣板',
            template=ConfirmTemplate(
                text='你確定要購買這項商品嗎？',
                actions=[
                    MessageTemplateAction(  # 按鈕選項
                        label='是',
                        text='@yes'
                    ),
                    MessageTemplateAction(
                        label='否',
                        text='@no'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendCarousel(event):  # 轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/4QfKuz1.png',
                        title='這是樣板一',
                        text='第一個轉盤樣板',
                        actions=[
                            MessageTemplateAction(
                                label='文字訊息一',
                                text='賣披薩'
                            ),
                            URITemplateAction(
                                label='連結文淵閣網頁',
                                uri='http://www.e-happy.com.tw'
                            ),
                            PostbackTemplateAction(
                                label='action sell 披薩',
                                data='action=sell&item=披薩'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/qaAdBkR.png',
                        title='這是樣板二',
                        text='第二個轉盤樣板',
                        actions=[
                            MessageTemplateAction(
                                label='文字訊息二',
                                text='賣飲料'
                            ),
                            URITemplateAction(
                                label='連結台大網頁',
                                uri='http://www.ntu.edu.tw'
                            ),
                            PostbackTemplateAction(
                                label='action sell 飲料',
                                data='action=sell&item=飲料'
                            ),
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendImgCarousel(event):  # 圖片轉盤
    try:
        message = TemplateSendMessage(
            alt_text='圖片轉盤樣板',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/4QfKuz1.png',
                        action=MessageTemplateAction(
                            label='文字訊息',
                            text='賣披薩'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://i.imgur.com/qaAdBkR.png',
                        action=PostbackTemplateAction(
                            label='回傳訊息',
                            data='action=sell&item=飲料'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendPizza(event):
    try:
        message = TextSendMessage(
            text='感謝您購買披薩，我們將盡快為您製作。'
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendYes(event):
    try:
        message = TextSendMessage(
            text='感謝您的購買，\n我們將盡快寄出商品。',
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendImgmap(event):  # 圖片地圖
    try:
        image_url = 'https://i.imgur.com/Yz2yzve.jpg'  # 圖片位址
        imgwidth = 1040  # 原始圖片寛度一定要1040
        imgheight = 300
        message = ImagemapSendMessage(
            base_url=image_url,
            alt_text="圖片地圖範例",
            base_size=BaseSize(height=imgheight, width=imgwidth),  # 圖片寬及高
            actions=[
                MessageImagemapAction(  # 顯示文字訊息
                    text='你點選了紅色區塊！',
                    area=ImagemapArea(  # 設定圖片範圍:左方1/4區域
                        x=0,
                        y=0,
                        width=imgwidth*0.25,
                        height=imgheight
                    )
                ),
                URIImagemapAction(  # 開啟網頁
                    link_uri='http://www.e-happy.com.tw',
                    area=ImagemapArea(  # 右方1/4區域(藍色1)
                        x=imgwidth*0.75,
                        y=0,
                        width=imgwidth*0.25,
                        height=imgheight
                    )
                ),
            ]
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！'))


def sendDatetime(event):  # 日期時間
    try:
        message = TemplateSendMessage(
            alt_text='日期時間範例',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/VxVB46z.jpg',
                title='日期時間示範',
                text='請選擇：',
                actions=[
                    DatetimePickerTemplateAction(
                        label="選取日期",
                        data="action=sell_date&mode=date",  # 觸發postback事件
                        mode="date",  # 選取日期
                        initial="2019-06-01",  # 顯示初始日期
                        min="2019-01-01",  # 最小日期
                        max="2020-12-31"  # 最大日期
                    ),
                    DatetimePickerTemplateAction(
                        label="選取時間",
                        data="action=sell_date&mode=time",
                        mode="time",  # 選取時間
                        initial="10:00",
                        min="00:00",
                        max="23:59"
                    ),
                    DatetimePickerTemplateAction(
                        label="選取日期時間",
                        data="action=sell_date&mode=datetime",
                        mode="datetime",  # 選取日期時間
                        initial="2019-06-01T10:00",
                        min="2019-01-01T00:00",
                        max="2020-12-31T23:59"
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！'))
