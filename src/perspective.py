import numpy as np

def getPerspective(points):
    points=np.squeeze(points)
    if len(points) <= 0:
        return ((0,0)) * 4


    a, b = getExtremes(points, (0, 1))
    c, d = getExtremes(points, (1, 0))

    if distSqr(a, b) > distSqr(c, d):
        far = (a, b)
    else:
        far = (c, d)

    near = (getExtremePointLine(points, far, min),
            getExtremePointLine(points, far, max))


    perspective = sortPerspectivePoints(far, near)

    return perspective



def getExtremePoint(points, order, strategies):
    extreme = points[0]
    for p in points:
        for s in order:
            if extreme[s] == p[s]:
                continue
            val = strategies[s](extreme[s], p[s])
            if val != extreme[s]:
                extreme = p
            break
    return extreme

def getExtremePointLine(points, line, strategy):
    extreme = ((pnt2line(points[0], line[0], line[1])[0]), points[0])
    for p in points:
        val = strategy(pnt2line(p, line[0], line[1])[0], extreme[0])
        if val != extreme[0]:
            extreme = (val, p)

    return extreme[1]


def distSqr(pa, pb):
        return (pa[0]-pb[0]) ** 2 + (pa[1]-pb[1]) ** 2

def getClosest(points, point):
    closest = (distSqr(points[0], point), points[0])
    for p in points:
        val = distSqr(p, point)
        if val < closest[0]:
            closest = (val, p)
    return closest[1]

def getExtremes(points, order):

    mins = (getExtremePoint(points, order, (min, min)),
            getExtremePoint(points, order, (min, max)))

    maxes = (getExtremePoint(points, order, (max, min)),
             getExtremePoint(points, order, (max, max)))


    maxPair = (0, ((0, 0), (0, 0)))

    for a in mins:
        for b in maxes:
            val = distSqr(a, b)
            if val > maxPair[0]:
                maxPair = (val, (a, b))

    return maxPair[1]


def sortPerspectivePoints(far, near):
    points = list(far) + list(near)
    left = getExtremePoint(points, (0,1), (min, min))
    right = getExtremePoint(points, (0,1), (max, max))
    width = right[0] - left[0]

    top = getExtremePoint(far, (1,0), (min, min))

    if top[0] - left[0] < width / 2:
        a = top
        b = getExtremePoint(near, (1,0), (max, min))
        c = getExtremePoint(far, (1,0), (max, max))
        d = getExtremePoint(near, (1,0), (min, max))
    else:
        a = getExtremePoint(near, (0,1), (min, min))
        b = top
        c = getExtremePoint(near, (0,1), (max, max))
        d = getExtremePoint(far, (1,0), (max, max))

    return (a,b,c,d)




def calcBoundaries(points):
    def minMaxPoint(oldP, newP, f):
        return (f(oldP[0], newP[0]), f(oldP[1], newP[1]))


    min_point = max_point = points[0]

    for p in points:
        min_point = minMaxPoint(min_point, p, min)
        max_point = minMaxPoint(max_point, p, max)
    return (min_point, max_point)




##################################################################
# FIXME: refactor this

import math

def dot(v,w):
    x,y = v
    X,Y = w
    return x*X + y*Y

def length(v):
    x,y = v
    return math.sqrt(x*x + y*y)

def vector(b,e):
    x,y = b
    X,Y = e
    return (X-x, Y-y)

def perp(b):
    x,y = b
    return (-y,x)

def unit(v):
    x,y = v
    mag = length(v)
    if mag == 0:
        return (1, 0)
    return (x/mag, y/mag)

def distance(p0,p1):
    return length(vector(p0,p1))

def scale(v,sc):
    x,y = v
    return (x * sc, y * sc)

def add(v,w):
    x,y = v
    X,Y = w
    return (x+X, y+Y)

def sub(v,w):
    x,y = v
    X,Y = w
    return (x-X, y-Y)


def pnt2line(pnt, start, end):
    line_vec = vector(start, end)
    pnt_vec = vector(start, pnt)
    line_len = length(line_vec)
    if line_len == 0:
        return (distance(pnt, start), start)
    line_unitvec = unit(line_vec)
    pnt_vec_scaled = scale(pnt_vec, 1.0/line_len)
    t = dot(line_unitvec, pnt_vec_scaled)
    nearest = scale(line_vec, t)
    dist = distance(nearest, pnt_vec)
    nearest = add(nearest, start)
    if (dot(perp(vector(start, pnt)), vector(start,end))) < 0:
        return (-dist, nearest)
    return (dist, nearest)
