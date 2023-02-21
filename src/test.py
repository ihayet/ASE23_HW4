from re import S
from SYM import SYM
from NUM import NUM
from strings import o, oo, show
from utils import getThe, rand, rnd, setSeed, get_ofile, copy, last
from repgrid import repcols, reprows, repplace, repgrid
from csv import csv
from DATA import DATA

def settings_test():
    err = 0
    val = oo(getThe())
    err += 1 if val != '{:Far 0.95 :Sample 512 :dump false :file etc/data/auto93.csv :go all :help false :min 0.5 :p 2 :seed 937162211}' else 0
    return 0

def rand_test():
    err = 0
    num1, num2 = NUM(), NUM()

    setSeed(getThe()['seed'])
    for i in range(1, 10**3):
        num1.add(rand(0, 1))
    
    setSeed(getThe()['seed'])
    for i in range(1, 10**3):
        num2.add(rand(0, 1))

    m1, m2 = rnd(num1.mid(), 10), rnd(num2.mid(), 10)

    if m1 != m2:
        err += 1
    if rnd(m1, 1) != 0.5:
        err += 1

    return err

def sym_test():
    err, sym = 0, SYM()
    for c in ["a","a","a","a","b","b","c"]:
        sym.add(c)
    
    if sym.mid() != "a":
        err += 1
    if sym.div() > (1.379 + 0.001) or sym.div() < (1.379 - 0.001):
        err += 1
    return err

def num_test():
    err, num = 0, NUM()
    for i in [1,1,1,1,2,2,3]:
        num.add(i)

    if num.mid() > (1.57142857 + 0.01) or num.mid() < (1.57142857 - 0.01):
        err += 1
    if rnd(num.div()) > (0.787 + 0.01) or rnd(num.div()) < (0.787 - 0.01):
        err += 1
    return err

def csv_test():
    err, n = 0, 0
    t = csv(getThe()['file'])

    for i in range(len(t)):
        for j in range(len(t[i])):
            n += 1
    if n != 8*399:
        err += 1
    return err

def data_test():
    err = 0
    data = DATA(getThe()['file'], None, None)
    err += 1 if len(data.rows) != 398 else 0
    err += 1 if data.cols.ycols[0].w != -1 else 0
    err += 1 if data.cols.xcols[0].col_pos != 0 else 0
    err += 1 if len(data.cols.xcols) != 4 else 0
    return err

def stats_test():
    err = 0
    res = ''
    data = DATA(getThe()['file'], None, None)
    for k, cols in zip(['y', 'x'], [data.cols.ycols, data.cols.xcols]):
        res += k + ' mid ' + o(data.stats('mid', cols, 2)) + '\n'
        res += ' ' + ' div ' + o(data.stats('div', cols, 2))
        if k != 'x': res += '\n'
    print(res)
    get_ofile().write(res + '\n')
    err += 1 if res != 'y mid {:Acc+ 15.57 :Lbs- 2970.42 :Mpg+ 23.84}\n  div {:Acc+ 2.76 :Lbs- 846.84 :Mpg+ 8.34}\nx mid {:Clndrs 5.45 :Model 76.01 :Volume 193.43 :origin 1}\n  div {:Clndrs 1.7 :Model 3.7 :Volume 104.27 :origin 1.3273558482394003}' else 0
    return err

def clone_test():
    err = 0
    data1 = DATA(getThe()['file'], None, None)
    data2 = data1.clone(data1.rows)
    err += 1 if len(data1.rows) != len(data2.rows) else 0
    err += 1 if data1.cols.ycols[0].w != data2.cols.ycols[0].w else 0
    err += 1 if data1.cols.xcols[0].get_pos() != data2.cols.xcols[0].get_pos() else 0
    err += 1 if len(data1.cols.xcols) != len(data2.cols.xcols) else 0
    return err

def around_test():
    err = 0
    o_file = get_ofile()
    data = DATA(getThe()['file'], None, None)
    
    around_dict = data.around(data.rows[0], None)
    
    pval = str(0) + ' ' + str(0) + ' ' + o(data.rows[0].cells)
    print(pval)
    o_file.write(pval + '\n')

    for n, (r, t) in enumerate(around_dict.items()):
        if n>0 and (n+1)%50==0:
            pval = str(n+1) + ' ' + str(rnd(t['dist'], 2)) + ' ' +  str(o(t['row'].cells))
            print(pval)
            o_file.write(pval + '\n')

    return err

def half_test():
    err = 0
    o_file = get_ofile()

    data = DATA(getThe()['file'], None, None)
    left, right, A, B, mid, c = data.half(None, None, None)
    
    pval = str(len(left)) + ' ' + str(len(right)) + ' ' + str(len(data.rows))
    print(pval)
    o_file.write(pval + '\n')
    
    pval = o(A.cells) + ' ' + str(c)
    print(pval)
    o_file.write(pval + '\n')

    pval = o(mid.cells)
    print(pval)
    o_file.write(pval + '\n')

    pval = o(B.cells)
    print(pval)
    o_file.write(pval + '\n')

    return err

def cluster_test():
    err = 0

    data = DATA(getThe()['file'], None, None)
    show(data.cluster(None, None, None, None), 'mid', data.cols.ycols, 1, None)

    return err

def optimize_test():
    err = 0

    data = DATA(getThe()['file'], None, None)
    show(data.sway(None, None, None, None), 'mid', data.cols.ycols, 1, None)

    return err

def copy_test():
    t1 = { 'a': 1, 'b': { 'c': 2, 'd': [3] } }
    t2 = copy(t1)
    t2['b']['d'][0] = 10000
            
    print('b4\t', end='')
    get_ofile().write('b4\t')
    oo(t1)
    print('\nafter\t')
    get_ofile().write('after\t')
    oo(t2)

    return 0

def repcols_test():
    t = repcols(getThe()['file'])
    
    try:
        for col in t.cols.xcols:
            print('{' + 'a NUM' + ' :at {}'.format(col.get_pos()) + ' :hi {}'.format(col.hi) + ' :lo {}'.format(col.lo) + ' :m2 {}'.format(rnd(col.m2, 3)) + ' :mu {}'.format(rnd(col.mu), 3) + ' :n {}'.format(col.total) + ' :txt {}'.format(col.get_name()) + '}')
            get_ofile().write('{' + 'a NUM' + ' :at {}'.format(col.get_pos()) + ' :hi {}'.format(col.hi) + ' :lo {}'.format(col.lo) + ' :m2 {}'.format(rnd(col.m2, 3)) + ' :mu {}'.format(rnd(col.mu), 3) + ' :n {}'.format(col.total) + ' :txt {}'.format(col.get_name()) + '}\n')
    except Exception:
        pass

    try:
        for row in t.rows:
            print('{' + 'a ROW :cells ' + str(row.cells) + '}')
            get_ofile().write('{' + 'a ROW :cells ' + str(row.cells) + '}\n')
    except Exception:
        pass

    return 0

def reprows_test():
    t = reprows(getThe()['file'])
    
    try:
        for col in t.cols.xcols:
            print('{' + 'a NUM' + ' :at {}'.format(col.get_pos()) + ' :hi {}'.format(col.hi) + ' :lo {}'.format(col.lo) + ' :m2 {}'.format(rnd(col.m2, 3)) + ' :mu {}'.format(rnd(col.mu), 3) + ' :n {}'.format(col.total) + ' :txt {}'.format(col.get_name()) + '}')
            get_ofile().write('{' + 'a NUM' + ' :at {}'.format(col.get_pos()) + ' :hi {}'.format(col.hi) + ' :lo {}'.format(col.lo) + ' :m2 {}'.format(rnd(col.m2, 3)) + ' :mu {}'.format(rnd(col.mu), 3) + ' :n {}'.format(col.total) + ' :txt {}'.format(col.get_name()) + '}\n')
    except Exception:
        pass

    try:
        for row in t.rows:
            print('{' + 'a ROW :cells ' + str(row.cells) + '}')
            get_ofile().write('{' + 'a ROW :cells ' + str(row.cells) + '}\n')
    except Exception:
        pass

    return 0

def synonyms_test():
    t = repcols(getThe()['file'])
    clustered = t.cluster(cols=t.cols.xcols)
    show(clustered)

    return 0

def prototypes_test():
    t = reprows(getThe()['file'])
    clustered = t.cluster(cols=t.cols.xcols)
    show(clustered)

    return 0

def position_test():
    t = reprows(getThe()['file'])
    clustered = t.cluster()
    
    repplace(clustered)

    return 0

def every_test():
    repgrid(getThe()['file'])

    return 0