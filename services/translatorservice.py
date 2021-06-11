from googletrans import Translator
from urllib.parse import quote


# https: // cloud.google.com/translate/docs/languages


def getTranslate(lang, mtext, sound):  # 翻譯及朗讀
    try:
        if lang.lower() == "zh":
            lang = "zh-TW"
        translator = Translator()
        # zh-TW, en, ja ...
        translation = translator.translate(mtext, dest=lang)

        if sound == 'yes':  # 發音
            # text = quote(translation["src"])
            stream_url = ""
            # print(stream_url)
            message = {
                "text": translation.text,
                "content_url": stream_url
            }
        else:  # 不發音
            message = {
                "text": translation
            }
        return message
    except Exception as e:
        pass
        # print(e)


if __name__ == "__main__":
    r = getTranslate("zh", "菜", True)
    # print(r["text"])
