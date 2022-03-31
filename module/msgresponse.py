from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, AudioSendMessage, VideoSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
baseurl = settings.STATIC_URL

imgMap = {
    "zhizhi": "https://i.imgur.com/IhQm1MI.png",
    "mouse": "https://i.imgur.com/LFqbHF8.png",
    "stable": "https://imgur.com/mDZ6PqN.png",
    "bad": "https://i.imgur.com/ZjrBz79.png",
    "cp": "https://imgur.com/YP48ccb.png",
}


def sendText(event, msg=None):  # 傳送文字
    try:
        if msg == None:
            return
        message = TextSendMessage(
            text=msg
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='請支援收銀!'))


def sendImage(event, key):  # 傳送圖片 https://i.imgur.com/IhQm1MI
    try:
        message = ImageSendMessage(
            original_content_url=imgMap[key],
            preview_image_url=imgMap[key]
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='請支援收銀!'))


def sendStick(event, stickObj):  # 傳送貼圖
    try:
        message = StickerSendMessage(  # 貼圖兩個id需查表
            package_id=stickObj["pid"],
            sticker_id=stickObj["sid"]
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='請支援收銀!'))


def sendMulti(event, msg=None, imgURL=None, stickObj=None):  # 多項傳送
    try:
        message = []
        if msg != None:
            message.append(TextSendMessage(  # 傳送y文字
                text=msg
            ))
        if imgURL != None:
            message.append(ImageSendMessage(  # 傳送圖片
                original_content_url=imgURL,
                preview_image_url=imgURL
            ))
        if stickObj != None:
            message.append(StickerSendMessage(  # 傳送貼圖 https://developers.line.biz/en/docs/messaging-api/sticker-list/
                package_id='446',
                sticker_id='1988'
            ))
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='請支援收銀!'))


def sendPosition(event):  # 傳送位置
    try:
        message = LocationSendMessage(
            title='101大樓',
            address='台北市信義路五段7號',
            latitude=25.034207,  # 緯度
            longitude=121.564590  # 經度
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='請支援收銀!'))


def sendQuickreply(event):  # 快速選單
    try:
        message = TextSendMessage(
            text='請選擇最喜歡的程式語言',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="Go", text="Go")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="Python", text="Python")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="Java", text="Java")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="C", text="C")
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='請支援收銀!'))


def sendVoice(event):  # 傳送聲音
    print(baseurl)
    try:
        message = AudioSendMessage(
            original_content_url=baseurl + 'video/mario.m4a',  # 聲音檔置於static資料夾
            duration=20000  # 聲音長度20秒
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='請支援收銀!'))


def sendVedio(event):  # 傳送影像
    try:
        message = VideoSendMessage(
            original_content_url=baseurl + 'video/robot.mp4',  # 影片檔置於static資料夾
            preview_image_url=baseurl + 'img/robot.jpg'
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='請支援收銀!'))
