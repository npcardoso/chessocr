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

        self.perspective_points = getPerspectivePoints(points)
        (x_min, x_max, y_min, y_max) = self.perspective_points

        self.ratio = calcRatio(self.boundaries)
        # FIXME: Calculate area using perspective points
        self.area = calcArea(self.boundaries)

    def drawHighlights(self, draw):
        p_min, p_max = self.boundaries
        draw.rectangle(list(p_min) + list(p_max), outline=tuple([0,128,128,128]))

        (x_min, x_max, y_min, y_max) = self.perspective_points
        draw.polygon((x_min, y_min, x_max, y_max), outline=tuple([255,0,255,128]))

    def extractArea(self, image, w, h):
        (x_min, x_max, y_min, y_max) = self.perspective_points


        # Find correct rotation (assuming image rotation angle is small)
        h_center = x_min[0] + ((x_max[0] - x_min[0]) / 2)
        if y_min[0] > h_center:
            pa = [y_max,
                  x_max,
                  y_min,
                  x_min]
        else:
            pa = [x_min,
                  y_max,
                  x_max,
                  y_min]

        pb = [(0,0),
              (w, 0),
              (w,h),
              (0, h)]

        print(pb, pa)

        coeffs = calcCoeffs(pb, pa)

        return image \
            .copy() \
            .transform((w, h), Image.PERSPECTIVE, coeffs, Image.BICUBIC)



def getPerspectivePoints(points):
    def getExtremePoint(points, rightmost=True, topmost=None):
        mult = -1
        if rightmost:
            mult = 1

        if topmost is None:
            topmost=not rightmost;

        mult2 = -1
        if topmost:
            mult2 = 1

        extreme = [points[0][0] * mult, points[0]]
        for p in points:
            val = p[0] * mult
            if val > extreme[0]:
                extreme = [val, p]
            elif val == extreme[0]:
                if p[1] * mult2 > extreme[1][1]:
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

    x_min, x_max = (getExtremePoint(points, False, False),
                    getExtremePoint(points, True, True))


    if x_min[1] > x_max[1]:
        x_min, x_max = (getExtremePoint(points, False, True),
                        getExtremePoint(points, True, False))



    y_min, y_max = (getExtremePointLine(points, (x_min, x_max), False),
                    getExtremePointLine(points, (x_min, x_max), True))

    return(x_min, x_max, y_min, y_max)




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
