from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, PostbackEvent
from module import msgresponse
from services import cwbservices, invoiceservice, covid19service, exchangeservice, cambridgeservice, nmnsservice, taiwanlotteryservice, gasservice, ivyservice, stockservice, githubservice
from urllib.parse import parse_qsl
from myconst import cmdlist
import re
from datetime import datetime, time
from decouple import config
from utility import timeUtility

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    try:
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
                        mtext = event.message.text.strip()
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
                        elif mtext == "壞":
                            msgresponse.sendImage(event, "bad")
                        elif mtext == "辛苦了" or mtext == "知道了":
                            msgresponse.sendImage(event, "cp")
                        elif mtext == "疫情":
                            resMsg = ""
                            startTime = time(13, 50)
                            endTime = time(16, 50)
                            currentTime = datetime.now().time()
                            if timeUtility.timeInRange(startTime, endTime, currentTime):
                                pttRes = covid19service.getGossipCovid19()
                                if len(pttRes) > 0:
                                    resMsg = "%s\n%s\n%s\n" % (
                                        pttRes["Date"], pttRes["Title"], pttRes["Link"])
                            else:
                                print("=== %s ~ %s 不抓 PTT 資料 ===" %
                                      (startTime, endTime))

                            officalRes = covid19service.getCovid19()
                            if officalRes != "":
                                nowDateEng = datetime.now().strftime("%b-%-d")
                                regex = re.compile(
                                    r'^Updated on '+nowDateEng+'.*')
                                if regex.match(officalRes["time"]) == None:
                                    resMsg += "\n= 你家的政府官網沒更新! =\n"
                            resMsg += "\n%s\n 新增確診:\t %s (本土 %s, 境外 %s) \n 新增死亡:\t %s\n 累計確診:\t %s\n 累計死亡:\t %s\n 死亡率:\t %s\n 疫苗接種人次:\t %s %s\n %s" % (
                                officalRes["time"], officalRes["recovered"], officalRes["domesticRecovered"], officalRes["internationalRecovered"], officalRes["newDeaths"], officalRes["total"], officalRes["totalDeaths"], officalRes["rateDeaths"], officalRes["vaccine"], officalRes["vaccinePercent"], officalRes["url"])
                            # 縣市
                            officalResList = ["\n%s:\t%s" %
                                              (k, v)for k, v in officalRes["countrysDict"].items()]
                            resMsg += "".join(officalResList)
                            if resMsg != "":
                                msgresponse.sendText(event, resMsg)
                        elif re.match(r"^匯率", mtext) != None:
                            msg = mtext.replace('匯率', '').strip()
                            resMsg = exchangeservice.toMsg(exchangeservice.getBoTExchange(
                                msg))
                            msgresponse.sendText(event, resMsg)
                        elif re.match(r".*bug.*", mtext) != None:
                            msgresponse.sendText(event, "請支援收銀~")
                        elif mtext == "cp下班":
                            msgresponse.sendImage(event, "cp2")
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
                            # 翻譯
                            msg = mtext.replace('t:', '').strip()
                            if msg != "":
                                resMsg = cambridgeservice.toMsg(
                                    cambridgeservice.transWord(msg), False)
                                msgresponse.sendText(event, resMsg)
                        elif re.match(r"^te:.*", mtext) != None:
                            # 翻譯 + 範例
                            msg = mtext.replace('te:', '').strip()
                            if msg != "":
                                resMsg = cambridgeservice.toMsg(
                                    cambridgeservice.transWord(msg), True)
                                msgresponse.sendText(event, resMsg)
                        elif mtext == "td:":
                            # 每日一句
                            resMsg = cambridgeservice.toMsg(
                                cambridgeservice.getDailyAWord(), True)
                            msgresponse.sendText(event, resMsg)
                        elif mtext == "穩":
                            msgresponse.sendImage(event, "stable")
                        elif mtext == "天文":
                            now = datetime.now()
                            resMsg, resImgURL = nmnsservice.getStarDayText(now)
                            msgresponse.sendMulti(event, resMsg, resImgURL)
                        elif mtext == "天文月":
                            msgresponse.sendText(
                                event, nmnsservice.getStarText())
                        elif mtext in ["樂透", "威力彩", "大樂透"]:
                            msgresponse.sendText(
                                event, taiwanlotteryservice.getlotteryText())
                        elif mtext == "油價":
                            msgresponse.sendText(
                                event, gasservice.getCPCText())
                        elif mtext == "三大":
                            res = stockservice.getThreeRrade()
                            if res == None:
                                return
                            resMsg = "%s\n%s\n%s" % (
                                res["title"], res["data"], res["url"])
                            msgresponse.sendText(event, resMsg)
                        elif re.match(r"^外資\s?\d{0,2}", mtext) != None:
                            nums = re.sub(r'\D', "", mtext)
                            if nums == "":
                                nums = 5
                            res = stockservice.getForeign(int(nums))
                            if res == None:
                                return
                            resMsg = "%s\n%s\n%s" % (
                                res["title"], res["data"], res["url"])
                            msgresponse.sendText(event, resMsg)
                        elif mtext == "event":
                            res = stockservice.getWeekEvent()
                            if res == None:
                                return
                            resMsg = "%s\n%s" % (
                                res["title"], res["data"])
                            msgresponse.sendText(event, resMsg)
                        elif mtext == "kimi" or mtext == "Kimi" or mtext == "蔡章章":
                            res = githubservice.getKimi0230()
                            if res == None:
                                return
                            resMsg = ("{} : {}".format(
                                "https://github.com/kimi0230", res))
                            msgresponse.sendText(event, resMsg)
                        elif re.match(r"^ivy\s?\d{0,2}", mtext) != None:
                            nums = re.sub(r'\D', "", mtext)
                            if nums == "":
                                nums = 3
                            msgresponse.sendText(
                                event, ivyservice.getLastNumsDaysText(nums=int(nums)))

                if isinstance(event, PostbackEvent):  # PostbackTemplateAction觸發此事件
                    # 取得Postback資料
                    pass

            return HttpResponse()

        else:
            return HttpResponseBadRequest()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()
