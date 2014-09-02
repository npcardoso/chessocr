import random
from PIL import Image

from floodfill import floodfill
from vectors import pnt2line
from perspective import calcCoeffs

class Area:
    def __init__(self, pix, start_point, bg, fg, boundaries):
        self.color = tuple([random.randint(1,255),
                             random.randint(1,255),
                             random.randint(1,255)])
        points = floodfill(pix, start_point , self.color, fg, boundaries)
        self.boundaries = calcBoundaries(points)

        self.ratio = calcRatio(self.boundaries)
        # FIXME: Calculate area using perspective points
        self.area = calcArea(self.boundaries)

        self.perspective_points = getPerspectivePoints(points)

    def drawHighlights(self, draw):
        p_min, p_max = self.boundaries
        draw.rectangle(list(p_min) + list(p_max), outline=tuple([0,128,128,128]))

        perspective =(a,b,c,d) = self.perspective_points
        draw.polygon((a, c), outline=tuple([255,0,0,128]))
        draw.polygon((b, d), outline=tuple([0,0,255,128]))

        draw.polygon(perspective, outline=tuple([255,0,255,128]))

    def extractArea(self, image, w, h):
        pa = self.perspective_points

        pb = [(0,0),
              (w, 0),
              (w,h),
              (0, h)]


        coeffs = calcCoeffs(pb, pa)

        return image \
            .copy() \
            .transform((w, h), Image.PERSPECTIVE, coeffs, Image.BICUBIC)


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


def getPerspectivePoints(points):
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

    return sortPerspectivePoints(far, near)





def calcBoundaries(points):
    def minMaxPoint(oldP, newP, f):
        return (f(oldP[0], newP[0]), f(oldP[1], newP[1]))


    min_point = max_point = points[0]

    for p in points:
        min_point = minMaxPoint(min_point, p, min)
        max_point = minMaxPoint(max_point, p, max)
    return (min_point, max_point)


def calcRatio (boundaries):
    p1, p2 = boundaries
    a, b = (p2[0] - p1[0]), (p2[1] - p1[1])
    if b == 0:
        return 0
    ret = a / float(b)
    if ret > 1:
        return 1 / ret
    return ret

def calcArea(boundaries):
    p1, p2 = boundaries
    return (p2[0] - p1[0]) * (p2[1] - p1[1])
