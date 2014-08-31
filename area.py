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
        self.true_boundaries = (getClosestPoint(points, self.boundaries[0]),
                                getClosestPoint(points, self.boundaries[1]))
        self.horizontal_boundaries = (getExtremePoint(points, False),
                                      getExtremePoint(points, True))
        self.vertical_boundaries = (getExtremePointLine(points, self.horizontal_boundaries, False),
                                    getExtremePointLine(points, self.horizontal_boundaries, True))
        self.ratio = calcRatio(self.boundaries)
        self.area = calcArea(self.boundaries)

    def drawHighlights(self, draw):
        p_min, p_max = self.boundaries
        draw.rectangle(list(p_min) + list(p_max), outline=tuple([0,128,128,128]))

        p_min, p_max = self.true_boundaries
        draw.rectangle(list(p_min) + list(p_max), outline=tuple([0, 255,0,128]))

        p_min, p_max = self.horizontal_boundaries
        draw.rectangle(list(p_min) + list(p_max), outline=tuple([0,0,255,128]))

        p_min_v, p_max_v = self.vertical_boundaries
        draw.polygon((p_min, p_min_v, p_max, p_max_v, p_min), outline=tuple([255,0,255,128]))

    def extractArea(self, image, w, h):
        h_bound = self.horizontal_boundaries
        v_bound = self.vertical_boundaries

        pa = [h_bound[0],
              v_bound[1],
              h_bound[1],
              v_bound[0]]

        pb = [(0,0),
              (w, 0),
              (w,h),
              (0, h)]

        coeffs = calcCoeffs(pb, pa)

        return image \
            .copy() \
            .transform((w, h), Image.PERSPECTIVE, coeffs, Image.BICUBIC)



def calcBoundaries(points):
    def minMaxPoint(oldP, newP, f):
        return (f(oldP[0], newP[0]), f(oldP[1], newP[1]))


    min_point = max_point = points[0]

    for p in points:
        min_point = minMaxPoint(min_point, p, min)
        max_point = minMaxPoint(max_point, p, max)
    return (min_point, max_point)

def calcDistSqr(p1, p2):
    return ((p1[0] - p2[0])**2) + ((p1[1] - p2[1]) ** 2)

def getClosestPoint(points, point):
    closest = [calcDistSqr(points[0], point), points[0]]
    for p in points:
        dist = calcDistSqr(p, point)
        if dist < closest[0]:
            closest = [dist, p]
    return closest[1]

def getExtremePoint(points, rightmost=True):
    mult = -1
    if rightmost:
        mult = 1

    extreme = [points[0][0] * mult, points[0]]
    for p in points:
        val = p[0] * mult
        if val > extreme[0]:
            extreme = [val, p]
        elif val == extreme[0]:
            if p[1] * mult > extreme[1][1]:
                extreme = [val, p]

    return extreme[1]

def getExtremePointLine(points, line, topmost=True):
    mult = -1
    if topmost:
        mult = 1

    extreme = [(pnt2line(points[0], line[0], line[1])[0]) * mult, points[0]]
    for p in points:
        val = (pnt2line(p, line[0], line[1])[0]) * mult
        if val > extreme[0]:
            extreme = [val, p]
        elif val == extreme[0]:
            if p[1] * mult > extreme[1][1]:
                extreme = [val, p]

    return extreme[1]


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
