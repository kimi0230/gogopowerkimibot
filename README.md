# GoGoPowerKimi

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
heroku logs --tail
```
## Reference
* https://github.com/henriquebastos/python-decouple
* https://ithelp.ithome.com.tw/articles/10209644