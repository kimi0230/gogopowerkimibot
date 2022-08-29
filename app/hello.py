from socket import MsgFlag
from django.http import HttpResponse
from ratelimit.decorators import ratelimit
import datetime
from django.contrib import admin
from django_redis import get_redis_connection
from django.views.decorators.cache import never_cache


@never_cache
@ratelimit(key='ip', rate='100/s', block=True)
def Hello(request):
    time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    expiry_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
    headers = {
        'Cache-Control': 'no-cache,max-age=0,no-store,s-maxage=0,proxy-revalidate',
        'Expires': expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
    }
    return HttpResponse("Hello Kimi ! \n " + time, headers=headers)


@never_cache
@ratelimit(key='ip', rate='1/s', block=True)
def Redis(request):
    # Use the name you have defined for Redis in settings.CACHES
    r = get_redis_connection("fly")
    msg = "Redis Check = %r" % (r.ping())
    print(msg)
    return HttpResponse(msg)


# 覆蓋預設的admin登入方法實現登入限流
@ratelimit(key='ip', rate='100/s', block=True)
def extend_admin_login(request, extra_context=None):
    return admin.site.login(request, extra_context)
