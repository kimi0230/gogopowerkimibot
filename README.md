# GoGoPowerKimi

## Commands
* `發票 {數字N: 代表前N期}`
* `天氣 {地區}`
* `疫情`
* `匯率 {幣別}`
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


## Command
```

```

## Heroku
1. runtime.txt
2. Procfile
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
heroku git:remote -a gogopowerkimibot 

# log
heroku login
heroku logs --tail
```

## Reference
* https://github.com/henriquebastos/python-decouple
* https://ithelp.ithome.com.tw/articles/10209644
* [中央氣象局opendata](https://opendata.cwb.gov.tw/index)
* [中央氣象局opendata 資料代碼](https://opendata.cwb.gov.tw/opendatadoc/MFC/ForecastElement.pdf)
* [統一發票](https://invoice.etax.nat.gov.tw/invoice.xml)