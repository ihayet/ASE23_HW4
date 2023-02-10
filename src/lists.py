from collections import OrderedDict

def map(t, fun):
    temp = {}
    for k, v in enumerate(t):
        v, k = fun(v)
        if k is None:
            temp[len(temp.keys())] = v
        else:
            temp[k] = v
    return temp

def kap(t, fun):
    temp = OrderedDict()
    for k, v in enumerate(t):
        v, k = fun(k, v)
        temp[k if k is not None else len(temp.keys())] = v
    return temp

def sort(t, k):
    if isinstance(t, dict):
        t = sorted(t.items(), key=lambda x: x[1][k])
    else:
        t = sorted(t.items())
    return t

def keys(t):
    ks = t.keys()
    ks.sort()
    return ks