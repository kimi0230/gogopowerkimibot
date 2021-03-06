from apscheduler.schedulers.blocking import BlockingScheduler
import urllib.request
from services import linenotifyservice
sched = BlockingScheduler()

# @sched.scheduled_job('cron', day_of_week='mon-fri', minute='*/20')


@sched.scheduled_job('interval', minutes=25)
def scheduled_job():
    url = "http://127.0.0.1:8000"
    conn = urllib.request.urlopen(url)

    for key, value in conn.getheaders():
        print(key, value)


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=18, minute='15')
def scheduled_job():
    linenotifyservice.stock5pm()


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=8, minute='38')
def scheduled_job():
    linenotifyservice.punchIn()


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17, minute='38')
def scheduled_job():
    linenotifyservice.punchOut()


sched.start()
