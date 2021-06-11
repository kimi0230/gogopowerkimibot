from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, PostbackEvent
from module import msgresponse
from services import cwbservices, invoiceservice
from urllib.parse import parse_qsl

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext == '卡比請客':
                        msgresponse.sendText(event, "謝謝卡比 讚嘆卡比 卡比讚讚讚")
                    elif mtext == '蔡章章的戶頭餘額':
                        stickObj = {
                            "pid": 11537
                            "sid": 52002759
                        }
                        msgresponse.sendStick(event, stickObj)
                    elif "bug" in mtext:
                        msgresponse.sendText(event, "請支援收銀~")
                    elif "吱吱" in mtext:
                        msgresponse.sendImage(event, "zhizhi")
                    elif mtext == "笑鼠人":
                        msgresponse.sendImage(event, "mouse")
                    elif "發票" in mtext:
                        resMsg = invoiceservice.getInvoice(mtext)
                        if resMsg != "":
                            msgresponse.sendText(event, resMsg)
                    elif "天氣" in mtext:
                        msg = mtext.replace('天氣', '')
                        cityArea = cwbservices.getCityArea(msg)
                        resMsg = ""
                        if cityArea["City"] != "":
                            resMsg += cwbservices.getWeather(
                                cityArea["City"]) + "\n"
                        if cityArea["Area"] != "":
                            if cityArea["Area"] == '板橋':
                                resMsg += "卡比請客\n"
                            resMsg += cwbservices.getAir(cityArea["Area"])
                        if resMsg != "":
                            msgresponse.sendText(event, resMsg)

            if isinstance(event, PostbackEvent):  # PostbackTemplateAction觸發此事件
                # 取得Postback資料
                pass

        return HttpResponse()

    else:
        return HttpResponseBadRequest()
