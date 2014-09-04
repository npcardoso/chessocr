import cv2
import numpy as np

from vectors import pnt2line

class Area:
    def __init__(self, color, pixels, pos, shape, start_point):
        self._color = color
        self._pixels = pixels
        self._shape = pos
        self._shape = shape
        self._boundaries = (pos, (pos[0] + shape[0], pos[1] + shape[1]))
        self._start_point = start_point

    def getColor(self):
        return self._color

    def getRatio(self):
        w, h = self._shape
        if h == 0:
            return 0
        ret = w / float(h)
        if ret > 1:
            return 1 / ret
        return ret

    def getBoundaries(self):
        return self._boundaries

    def getArea(self):
        w, h = self._shape
        return w * h


    def getPerspective(self, image):
        if self._pixels <= 0:
            return ((0,0)) * 4

        (x, y), (xx, yy) = self._boundaries

        points = np.where((image[y:yy, x:xx] == self._color))

        xx = [i + x for i in points[1]]
        yy = [i + y for i in points[0]]


        points = tuple(zip(xx, yy))
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
