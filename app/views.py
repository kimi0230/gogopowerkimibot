from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, PostbackEvent
from module import msgresponse
from services import cwbservices, invoiceservice, covid19service, exchangeservice, cambridgeservice, nmnsservice
from urllib.parse import parse_qsl
from myconst import cmdlist
import re

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
                    elif mtext == "ls":
                        msgresponse.sendText(event, cmdlist.CMD_LIST)
                    elif mtext == '蔡章章戶頭':
                        stickObj = {
                            "pid": 11537,
                            "sid": 52002759
                        }
                        msgresponse.sendStick(event, stickObj)
                    elif mtext == "笑鼠人":
                        msgresponse.sendImage(event, "mouse")
                    elif mtext == "疫情":
                        pttRes = covid19service.getGossipCovid19()
                        resMsg = ""
                        if len(pttRes) > 0:
                            resMsg = "%s\n%s\n%s\n" % (
                                pttRes["Date"], pttRes["Title"], pttRes["Link"])
                        res = covid19service.getCovid19()
                        resMsg += "\n%s\n 新增確診:\t %s\n 新增死亡:\t %s\n 累計確診:\t %s\n 累計死亡:\t %s\n 死亡率:\t %s\n 疫苗接種人次:\t %s\n %s" % (
                            res["time"], res["recovered"], res["newDeaths"], res["total"], res["totalDeaths"], res["rateDeaths"], res["vaccine"], res["url"])
                        if resMsg != "":
                            msgresponse.sendText(event, resMsg)
                    elif re.match(r"^匯率", mtext) != None:
                        msg = mtext.replace('匯率', '').strip()
                        res = exchangeservice.getBoTExchange(msg)
                        if res != "":
                            resMsg = "|幣別\t\t|即期買\t|即期賣\t|\n"
                            for r in res:
                                resMsg += "|%s | %s | %s |\n" % (
                                    r, res[r][2], res[r][3])
                            resMsg += "https://rate.bot.com.tw/xrt?Lang=zh-TW"
                            msgresponse.sendText(event, resMsg)
                    elif re.match(r".*bug.*", mtext) != None:
                        msgresponse.sendText(event, "請支援收銀~")
                    elif mtext == "吱吱":
                        msgresponse.sendImage(event, "zhizhi")
                    elif re.match(r".*發票.*", mtext) != None:
                        resMsg = invoiceservice.getInvoice(mtext)
                        if resMsg != "":
                            msgresponse.sendText(event, resMsg)
                    # elif re.match(r".*天氣.*", mtext) != None:
                    #     msg = mtext.replace('天氣', '')
                    #     cityArea = cwbservices.getCityArea(msg)
                    #     resMsg = ""
                    #     if cityArea["City"] != "":
                    #         resMsg += cwbservices.getWeather(
                    #             cityArea["City"]) + "\n"
                    #     if cityArea["Area"] != "":
                    #         if cityArea["Area"] == '板橋':
                    #             resMsg += "卡比請客\n"
                    #         resMsg += cwbservices.getAir(cityArea["Area"])
                    #     if resMsg != "":
                    #         msgresponse.sendText(event, resMsg)
                    elif re.match(r"^t:.*", mtext) != None:
                        msg = mtext.replace('t:', '').strip()
                        if msg != "":
                            resMsg = cambridgeservice.toMsg(
                                cambridgeservice.transWord(msg), False)
                        if resMsg != "":
                            msgresponse.sendText(event, resMsg)
                    elif re.match(r"^te:.*", mtext) != None:
                        msg = mtext.replace('te:', '').strip()
                        if msg != "":
                            resMsg = cambridgeservice.toMsg(
                                cambridgeservice.transWord(msg), True)
                        if resMsg != "":
                            msgresponse.sendText(event, resMsg)
                    elif mtext == "td:":
                        resMsg = cambridgeservice.toMsg(
                            cambridgeservice.getDailyAWord(), True)
                        if resMsg != "":
                            msgresponse.sendText(event, resMsg)
                    elif mtext == "穩":
                        msgresponse.sendImage(event, "stable")
                    elif mtext == "天文":
                        msgresponse.sendText(nmnsservice.getStarText(), resMsg)
            if isinstance(event, PostbackEvent):  # PostbackTemplateAction觸發此事件
                # 取得Postback資料
                pass

        return HttpResponse()

    else:
        return HttpResponseBadRequest()
