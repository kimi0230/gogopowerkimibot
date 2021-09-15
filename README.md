# GoGoPowerKimi

LINE 機器人, LINE Notify.
使用 Django, Django Q 排程, PostgreSQL, GitHub Active 自動部署至 Heroku
發票, 天氣, 匯率, 疫情, ptt 爬蟲, [Cambridge Dictionary](https://dictionary.cambridge.org/zht)爬蟲
中油油價漲幅 notify
每日英文單字 notify 等

![line bot](https://github.com/kimi0230/gogopowerkimibot/blob/master/images/gif/bot.gif)
![line notify](https://github.com/kimi0230/gogopowerkimibot/blob/master/images/gif/notify.gif)
## Commands

- `發票 {數字N}`: N:代表前 N 期的發票(optinal) ex. `發票 1`
- ~~`天氣 {地區}`: 地區:縣市區(required) ex. 天氣汐止~~
- `疫情`: 台灣疫情資訊
- `匯率 {幣別}`: ex. 匯率 美金
- `卡比請客`
- `笑鼠人`
- `吱吱`
- `蔡章章戶頭`
- `t:{英文單字}`: 取得翻譯 音標 詞性
- `te:{英文單字}`: 取得翻譯 音標 詞性 中英例句
- `td:`: 取得每日一單字
- `ls` : 顯示所有指令
- `天文`: 當月天文景象 https://www.nmns.edu.tw/learn/feature/star/2021/202109/
- `樂透`: 威力彩, 大樂透

## Install package

```shell
pip3 install -r requirements.txt
```

## Apply for LINE dev account

https://developers.line.biz/en/

## Migration

```shell
# create
python3 manage.py makemigrations

# sync
python3 manage.py migrate
```

## Set up Https by ngrok

LINE bot user webhook url as a link to server. 1. require url not IP address. 2. must https.

https://ngrok.com/download

## Run server

```shell
# 將靜態文件收集到STATIC_ROOT中
python3 manage.py collectstatic
python3 manage.py runserver
./ngrok http 8000
```

## Allow hosts

`linebot_practise/settings.py`

```python
ALLOWED_HOSTS = ['127.0.0.1', '20af8c34126e.ngrok.io']
```

## Add Webhook URL

![ngrok](https://github.com/kimi0230/linebot_practise/blob/master/screenshot/ngrok.png)
![webhook](https://github.com/kimi0230/linebot_practise/blob/master/screenshot/webhook.png)

## Heroku

1. runtime.txt
2. Procfile : 告訴 Heroku 伺服器種類及主程式名稱
3. gogopowerkimibot/prod_settings.py

### Heroku 免費限制 
1. 每 30 分鐘沒使用就會停機
    * Django Q 排程, 設定每25分鐘, 呼叫一次api避免休眠
2. 免費 550 小時
    * 可以驗證信用卡增加 450 小時
    * 因為加了排程會導致時間使用超過, 可以設定凌晨時不呼叫排成,讓他停機. 然後使用 github的workflows, 建立排程在早上喚醒

```shell
## install
pip3 install virtualenv

## create env
virtualenv herokuenv

cd herokuenv
## start env
source bin/activate
## stop env
deactivate

pip3 install dj-database-url dj-static gunicorn psycopg2-binary
pip freeze > requirements.txt

heroku config:set DJANGO_SETTINGS_MODULE=gogopowerkimibot.prod_settings
heroku config:set DISABLE_COLLECTSTATIC=1
heroku config:add TZ="Asia/Taipei"
heroku git:remote -a gogopowerkimibot

# bash
heroku run bash

# log
heroku login
heroku logs --tail
```

## Apply for notify token

https://notify-bot.line.me/my/

## Schedule tool: Django Q

1. `pip3 install django-q`
2. settings.py > INSTALLED_APPS > add `django_q`
3. `python3 manage.py migrate`
4. settings.py > INSTALLED_APPS > add `Q_CLUSTER` :https://django-q.readthedocs.io/en/latest/configure.html#orm-configuration

```python
# settings.py example
Q_CLUSTER = {
    'name': 'myproject',
    'workers': 8,
    'recycle': 500,
    'timeout': 60,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'label': 'Django Q',
    'redis': {
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0, }
}

Q_CLUSTER = {
    'name': 'gogopowerkimibot',
    'workers': 1,
    'timeout': 600,
    'retry': 1200,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default'
}
```

5. `python3 manage.py qcluster`

## Reference

- https://github.com/henriquebastos/python-decouple
- https://ithelp.ithome.com.tw/articles/10209644
- [中央氣象局 opendata](https://opendata.cwb.gov.tw/index)
- [中央氣象局 opendata 資料代碼](https://opendata.cwb.gov.tw/opendatadoc/MFC/ForecastElement.pdf)
- [統一發票](https://invoice.etax.nat.gov.tw/invoice.xml)
- https://django-q.readthedocs.io/en/latest/cluster.html
- https://github.com/chubin/wttr.in

## memo

```
python3 manage.py createsuperuser
python3 manage.py showmigrations
python3 manage.py migrate django_q zero
python3 -B -m services.linenotifyservice
```
