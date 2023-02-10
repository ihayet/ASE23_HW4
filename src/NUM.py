from VAL import VAL
from utils import rnd
import math
import re

class NUM(VAL):
    def __init__(self, *args):
        if len(args) > 0: 
            super().__init__(args[0], args[1])
            self.w = -1 if len(re.findall(r'-$', args[1])) > 0 else 1
        self.total, self.mu, self.m2 = 0, 0, 0
        self.lo, self.hi = math.inf, -math.inf

    def add(self, x):
        if x != '?':
            self.total += 1
            temp = x - self.mu
            self.mu += temp/self.total
            self.m2 += temp*(x - self.mu)
            self.lo = min(x, self.lo)
            self.hi = max(x, self.hi)

    def mid(self):
        return self.mu

    def div(self):
        return 0 if (self.m2 < 0 or self.total < 2) else (self.m2/(self.total-1))**0.5

    def rnd(self, x, n):
        return x if x=='?' else rnd(x, n)

    def norm(self, n):
        if n=='?':
            return n
        else:
            val = (n-self.lo)/(self.hi-self.lo + 1e-32)
        return val

    def dist(self, n1, n2):
        if n1=='?' and n2=='?':
            return 1
        n1, n2 = self.norm(n1), self.norm(n2)
        if n1=='?':
            n1 = 1 if n2<0.5 else 0
        if n2=='?':
            n2 = 1 if n1<0.5 else 0
        return abs(n1-n2)
