"""
source from https://github.com/jwenjian/visitor-badge
"""
from hashlib import md5
from pybadges import badge
import requests
import datetime
from django.http import HttpResponse
from ratelimit.decorators import ratelimit
from decouple import config
import re


def invalid_count_resp(err_msg):
    """
    Return a svg badge with error info when cannot process repo_id param from request
    :return: A response with invalid request badge
    """
    svg = badge(left_text="Error", right_text=err_msg,
                whole_link="https://github.com/jwenjian/visitor-badge")
    expiry_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)

    headers = {'Cache-Control': 'no-cache,max-age=0',
               'Expires': expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")}

    return HttpResponse(svg, content_type="image/svg+xml", headers=headers)


def update_counter(key):
    url = 'https://api.countapi.xyz/hit/visitor-badge/{0}'.format(key)
    try:
        resp = requests.get(url)
        if resp and resp.status_code == 200:
            return resp.json()['value']
        else:
            return None
    except Exception as e:
        return None


def identity_request_source(request):
    page_id = request.GET.get('page_id')
    print("!!!!!!", request.GET.get('page_id'))
    if page_id is not None and len(page_id):
        m = md5(page_id.encode('utf-8'))
        m.update(config(
            'MD5_KEY', default='guess_kimi').encode('utf-8'))
        return m.hexdigest()
    return None


@ratelimit(key='ip', rate='10/s', block=True)
@ratelimit(key='get:page_id', rate='5/s', block=True)
def visitor_svg(request):
    """
    Return a svg badge with latest visitor count of 'Referer' header value

    :return: A svg badge with latest visitor count
    """
    expiry_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)
    headers = {'Cache-Control': 'no-cache,max-age=0,no-store,s-maxage=0,proxy-revalidate',
               'Expires': expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")}
    req_source = identity_request_source(request)

    if not req_source:
        return invalid_count_resp('Missing required param: page_id')

    if re.match(r"^kimi0230\.{0,1}.*", request.GET.get('page_id')) == None:
        # https://steel-quark-crabapple.glitch.me/badge?page_id=kimi0230
        return HttpResponse('Please try : https://steel-quark-crabapple.glitch.me/badge?page_id=xxx or https://visitor-badge.glitch.me/badge?page_id=kimi0230', headers=headers)

    latest_count = update_counter(req_source)

    if not latest_count:
        return invalid_count_resp("Count API Failed")

    # get left color and right color
    left_color = "#595959"
    if request.GET.get("left_color") is not None:
        left_color = request.GET.get("left_color")

    right_color = "#1283c3"
    if request.GET.get("right_color") is not None:
        right_color = request.GET.get("right_color")

    left_text = "visitors"
    if request.GET.get("left_text") is not None:
        left_text = request.GET.get("left_text")

    svg = badge(left_text=left_text, right_text=str(latest_count),
                left_color=str(left_color), right_color=str(right_color))

    return HttpResponse(svg, content_type="image/svg+xml", headers=headers)
