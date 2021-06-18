from apscheduler.schedulers.blocking import BlockingScheduler
import urllib.request

sched = BlockingScheduler()

# @sched.scheduled_job('cron', day_of_week='mon-fri', minute='*/20')


@sched.scheduled_job('interval', minutes=25)
def scheduled_job():
    # url = "http://127.0.0.1:8000"
    url = "https:gogopowerkimibot.herokuapp.com/"
    conn = urllib.request.urlopen(url)

    for key, value in conn.getheaders():
        print(key, value)


sched.start()
