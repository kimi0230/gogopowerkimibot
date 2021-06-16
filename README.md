# GoGoPowerKimi

## Commands
* `發票 {數字N}`: N:代表前N期的發票(optinal) ex. `發票 1`
* `天氣 {地區}`: 地區:縣市區(required) ex. 天氣汐止
* `疫情`: 台灣疫情資訊
* `匯率 {幣別}`: ex. 匯率 美金
* `卡比請客`
* `笑鼠人`
* `吱吱`
* `蔡章章戶頭`
* `ls`  : 顯示所有指令

## Install package
``` shell
pip3 install -r requirements.txt
```

## Apply for LINE dev account
https://developers.line.biz/en/

## Migration
``` shell
# create 
python3 manage.py makemigrations

# sync
python3 manage.py migrate
```

## Set up Https by ngrok
LINE bot user webhook url as a link to server.
    1. require url not IP address.
    2. must https.

https://ngrok.com/download

## Run server
``` shell
# 將靜態文件收集到STATIC_ROOT中
python3 manage.py collectstatic
python3 manage.py runserver 
./ngrok http 8000
```

## Allow hosts
`linebot_practise/settings.py`

``` python
ALLOWED_HOSTS = ['127.0.0.1', '20af8c34126e.ngrok.io']
```

## Add Webhook URL
![ngrok](https://github.com/kimi0230/linebot_practise/blob/master/screenshot/ngrok.png)
![webhook](https://github.com/kimi0230/linebot_practise/blob/master/screenshot/webhook.png)

## Heroku
1. runtime.txt
2. Procfile : 告訴 Heroku 伺服器種類及主程式名稱
3. gogopowerkimibot/prod_settings.py

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
``` python
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
* https://github.com/henriquebastos/python-decouple
* https://ithelp.ithome.com.tw/articles/10209644
* [中央氣象局opendata](https://opendata.cwb.gov.tw/index)
* [中央氣象局opendata 資料代碼](https://opendata.cwb.gov.tw/opendatadoc/MFC/ForecastElement.pdf)
* [統一發票](https://invoice.etax.nat.gov.tw/invoice.xml)
* https://django-q.readthedocs.io/en/latest/cluster.html