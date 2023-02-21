import math
from lists import kap

the = {}
o_file = None

Seed=937162211
def rint(lo, hi):
    randval = math.floor(0.5 + rand(lo, hi))
    return randval

def setSeed(val):
  global Seed
  Seed = val

def rand(lo, hi):
  global Seed
  Seed = (16807 * Seed) % 2147483647
  divval = Seed/2147483647
  randvalrand = rnd(lo + (hi-lo) * divval, 9)
  return randvalrand

def rnd(n, nPlaces=3):
  return round(n, nPlaces)

def getThe():
  global the 
  return the

def setThe(options):
  global the
  the = options

def get_ofile():
  global o_file
  if o_file is None:
    o_file = open('etc/out', 'w', encoding='utf-8')
    
  return o_file

def any(t):
  if t is not None and len(t) > 0:
    randval = rint(len(t), 1) - 1
    
    if randval > len(t)-1:
      randval = len(t) - 1
    elif randval < 0:
      randval = 0
    
    return t[randval]
  else:
    return None

def many(t, sample_size):
  u = []
  for i in range(0, sample_size):
    val = any(t)
    if val is not math.inf:
      u.append(val)
  return u

def last(t):
  return t[len(t)-1]

def cosine(a, b, c):
  x1 = (a**2 + c**2 - b**2)/(2*c+1e-32)
  x2 = max(0, min(1, x1))
  y = abs(a**2 - x2**2)**0.5
  return x2, y

def copy(t):
  def fun(k, v):
    return copy(v), copy(k)
  
  if isinstance(t, dict) or isinstance(t, list):
    u = kap(t, fun)
    return u
  else:
    return t