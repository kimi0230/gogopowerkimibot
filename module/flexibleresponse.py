from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage, BubbleContainer, ImageComponent, BoxComponent, TextComponent, IconComponent, ButtonComponent, SeparatorComponent, FlexSendMessage, URIAction

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def sendFlex(event):  # 彈性配置
    try:
        bubble = BubbleContainer(
            direction='ltr',  # 項目由左向右排列 rtl(由右向左). default: ltr
            header=BoxComponent(  # 標題
                layout='vertical',
                contents=[
                    TextComponent(text='冰火飲料', weight='bold', size='xxl'),
                ]
            ),
            hero=ImageComponent(  # 主圖片
                url='https://i.imgur.com/3sBRh08.jpg',
                size='full',
                aspect_ratio='792:555',  # 長寬比例
                aspect_mode='cover',
            ),
            body=BoxComponent(  # 主要內容
                layout='vertical',  # required
                contents=[  # required
                    TextComponent(
                        text='評價',  # required
                        size='md'
                    ),
                    BoxComponent(
                        layout='baseline',  # 水平排列
                        margin='md',
                        contents=[
                            IconComponent(
                                size='lg', url='https://i.imgur.com/GsWCrIx.png'),
                            TextComponent(text='25   ', size='sm',
                                          color='#999999', flex=0),
                            IconComponent(
                                size='lg', url='https://i.imgur.com/sJPhtB3.png'),
                            TextComponent(text='14', size='sm',
                                          color='#999999', flex=0),
                        ]
                    ),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(
                                        text='營業地址:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(
                                        text='台北市信義路14號', color='#666666', size='sm', flex=5)
                                ],
                            ),
                            SeparatorComponent(color='#0000FF'),  # 分隔線
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(
                                        text='營業時間:', color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(
                                        text="10:00 - 23:00", color='#666666', size='sm', flex=5),
                                ],
                            ),
                        ],
                    ),
                    BoxComponent(
                        layout='horizontal',
                        margin='xxl',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                height='sm',
                                action=URIAction(
                                    label='電話聯絡', uri='tel:0987654321'),
                            ),
                            ButtonComponent(
                                style='secondary',
                                height='sm',
                                action=URIAction(
                                    label='查看網頁', uri="http://www.e-happy.com.tw")
                            )
                        ]
                    )
                ],
            ),
            footer=BoxComponent(  # 底部版權宣告
                layout='vertical',
                contents=[
                    TextComponent(text='Copyright@ehappy studio 2019',
                                  color='#888888', size='sm', align='center'),
                ]
            ),
        )
        message = FlexSendMessage(alt_text="彈性配置範例", contents=bubble)
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！'))


def manageForm(event, mtext):
    try:
        flist = mtext[3:].split('/')
        text1 = '姓名：' + flist[0] + '\n'
        text1 += '日期：' + flist[1] + '\n'
        text1 += '包廂：' + flist[2]
        message = TextSendMessage(
            text=text1
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='發生錯誤！'))
