from collections import OrderedDict
from ROW import ROW

def map(t, fun):
    if isinstance(t, dict):
        temp = {}
        for k, v in t.items():
            v, k = fun(v)
            
            if k is not None: temp[k] = v
            else: temp.append(v)
    elif isinstance(t, list):
        temp = []
        for k, v in enumerate(t):
            v, k = fun(v)
            
            if k is not None: temp[k] = v
            else: temp.append(v)
    return temp

def kap(t, fun):
    if isinstance(t, dict):
        temp = {}
        for k, v in t.items():
            v, k = fun(k, v)
            temp[k if k is not None else len(temp.keys())] = v
    elif isinstance(t, list):
        temp = [None] * len(t)
        for k, v in enumerate(t):
            v, k = fun(k, v)
            temp[k if k is not None else len(temp)] = v
    return temp

def sort(t, k):
    if isinstance(t, dict):
        t = sorted(t.items(), key=lambda x: x[1][k])
    else:
        t = sorted(t, key=lambda x: x[k])
    return t

def keys(t):
    ks = t.keys()
    ks.sort()
    return ks