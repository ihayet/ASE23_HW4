from COLS import COLS
from ROW import ROW
from csv import csv
from lists import map, kap, sort
from utils import getThe, cosine, many, any, last
import math

class DATA:
    def __init__(self, src, cols=None, rows=None):
        self.rows, self.cols = [], None
        map(csv(src), lambda x: self.add(x)) if src is not None else map(cols+rows, lambda x: self.add(x))            

    def add(self, t):
        if not self.cols is None:
            t = t if isinstance(t, ROW) else ROW(t)
            self.rows.append(t)
            self.cols.add(t)
        else:
            self.cols = COLS(t)
        return t, None

    def clone(self, rows):
        data = DATA(None, [self.cols.names], [row.get_cells() for row in (rows if rows is not None else self.rows)])
        return data

    def stats(self, what, cols, nPlaces):
        def fun(k, col): return col.rnd(col.mid() if (what == 'mid') else col.div(), nPlaces), col.get_name()
        return kap(self.cols.ycols if (cols is None or len(cols) == 0) else cols, fun)
    
    def better(self, row1, row2):
        s1, s2, ys = 0, 0, self.cols.ycols
        x, y = 0, 0
        for _, col in enumerate(ys):
            x = col.norm(row1.cells[col.get_pos()])
            y = col.norm(row2.cells[col.get_pos()])
            s1 = s1 - math.exp(col.w * (x-y)/len(ys))
            s2 = s2 - math.exp(col.w * (y-x)/len(ys))
        return s1/len(ys) < s2/len(ys)

    def dist(self, row1, row2, cols):
        n, d = 0, 0
        for _, col in enumerate(cols if cols is not None else self.cols.xcols):
            n += 1
            d += col.dist(row1.cells[col.get_pos()], row2.cells[col.get_pos()])**getThe()['p']
        val = (d/n)**(1/getThe()['p'])
        return val

    def around(self, row1, rows):
        def fun(row2):
            ret = dict()
            ret['row'] = row2
            ret['dist'] = self.dist(row1, row2, self.cols.xcols)
            return ret, None
        
        mapped_val = map(rows if rows is not None else self.rows, fun)
        sorted_val = sort(mapped_val, 'dist')

        return sorted_val

    def furthest(self, row1, rows):
        t = self.around(row1, rows)
        return t[len(t)-1]

    def half(self, rows, cols, above):
        A, B, c = 0, 0, 0
        left, right = [], []
        def project(row):
            x, y = cosine(self.dist(row, A, cols), self.dist(row, B, cols), c)
            ret = {}
            row.x, row.y = x, y
            ret['row'] = row
            ret['dist'] = x
            return ret, None
        rows = rows if rows is not None else self.rows
                
        A = above if above is not None else any(self.rows)
        B = self.furthest(A, rows)['row']
        c = self.dist(A, B, None)
        
        temp = sort(map(rows, project), 'dist')
        for n, t in enumerate(temp):
            if n < math.floor(len(rows)/2):
                left.append(t['row'])
                mid = t['row']
            else:
                right.append(t['row'])
        return left, right, A, B, mid, c

    def cluster(self, rows=None, cols=None, above=None):
        rows = rows if rows is not None else self.rows
        cols = cols if cols is not None else self.cols.xcols    

        newrows = []
        for row in rows:
            r = ROW([val for val in row.cells])
            r.x, r.y = row.x, row.y
            newrows.append(r)

        node = {
            'data': newrows
        }       
        
        if len(rows) >= 2:
            left, right, node['A'], node['B'], node['mid'], node['c'] = self.half(rows, cols, above)
            
            node['left'] = self.cluster(left, cols, node['A'])
            node['right'] = self.cluster(right, cols, node['B'])
        
        return node

    def sway(self, rows, min, cols, above):
        rows = rows if rows is not None else self.rows
        min = min if min is not None else len(rows)**getThe()['min']
        cols = cols if cols is not None else self.cols.xcols
        node = {
            'data': self.clone(rows)
        }

        if len(rows) > 2*min:
            left, right, node['A'], node['B'], node['mid'], c = self.half(rows, cols, above)
            if self.better(node['B'], node['A']):
                left, right, node['A'], node['B'] = right, left, node['B'], node['A']
            node['left'] = self.sway(left, min, cols, node['A'])

        return node