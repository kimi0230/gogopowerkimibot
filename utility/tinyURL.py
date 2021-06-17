
import contextlib
from urllib.parse import urlencode
from urllib.request import urlopen


def makeTiny(url):
    requestURL = ("http://tinyurl.com/api-create.php?"+urlencode({'url': url}))
    with contextlib.closing(urlopen(requestURL)) as response:
        return response.read().decode('utf-8')


if __name__ == "__main__":
    print(makeTiny("https://google.com"))
