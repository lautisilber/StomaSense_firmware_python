# copied from https://github.com/rcolistete/MicroPython_Statistics

import math

def mean(data):
    if iter(data) is data:
        data = list(data)
    return sum(data)/len(data)

def _ss(data, c=None):
    if c is None:
        c = mean(data)
    total = total2 = 0
    for x in data:
        total += (x - c)**2
        total2 += (x - c) 
    total -= total2**2/len(data)
    return total

def variance(data, xbar=None):
    if iter(data) is data:
        data = list(data)
    return _ss(data, xbar)/(len(data) - 1)

def stdev(data, xbar=None):
    return math.sqrt(variance(data, xbar))


# this is by me

def mean_and_stdev(data: list[float]) -> tuple[float, float]:
    n = len(data)
    m = sum(data) / n

    # _ss
    total = total2 = 0
    for x in data:
        t = (x - m)
        total += t * t
        total2 += t
    total -= (total2*total2)/n

    var = total/(n - 1)

    stdev = math.sqrt(var)

    return m, stdev
