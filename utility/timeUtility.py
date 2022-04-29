import datetime


def timeInRange(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


if __name__ == "__main__":
    start = datetime.time(23, 0, 0)
    end = datetime.time(1, 0, 0)
    currentTime = datetime.datetime.now().time()
    print(currentTime)
    print(timeInRange(start, end, datetime.time(23, 30, 0)))
    print(timeInRange(start, end, datetime.time(12, 30, 0)))
    print(timeInRange(datetime.time(13, 30), datetime.time(15, 40), currentTime))
