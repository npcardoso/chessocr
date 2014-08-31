import sys
from vectors import *
from PIL import Image, ImageFilter, ImageStat, ImageDraw
import random


def inside(x, boundaries):
    for i in range(len(x)):
        if x[i] < boundaries[0][i] or \
           x[i] > boundaries[1][i]:
            return False
    return True


def neighbors(p, boundaries):
    deltas = [[0,1], [1,0],
              [0,-1], [-1,0],
              [1,1], [1,-1],
              [1,-1], [-1,-1]]
    ret = []
    for d in deltas:
        pp = [p[0] + d[0], p[1] + d[1]]
        if inside(pp, boundaries):
            ret.append(pp)
    return ret


def floodFill (pix, point, color, fg, boundaries):
    x, y = point
    if pix[x, y] != fg:
        return 0

    pix[x, y] = color

    queue = [point]
    points = [point]

    while(queue):
        el = queue.pop()
        for x, y in neighbors(el, boundaries):
            if pix[x, y] == fg:
                pix[x, y] = color
                p = (x,y)
                queue.append(p)
                points.append(p)

    return points


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

def countOccur(pix, color, boundaries):
    min_point, max_point = boundaries
    ret = 0

    for x in range(min_point[0], max_point[0]):
        for y in range(min_point[1], max_point[1]):
            if pix[x, y] == color:
                ret += 1
    return ret


class Area:
    def __init__(self, pix, start_point, bg, fg, boundaries):
        self.color = tuple([random.randint(1,255),
                             random.randint(1,255),
                             random.randint(1,255)])
        points = floodFill(pix, start_point , self.color, fg, boundaries)
        self.boundaries = calcBoundaries(points)
        self.true_boundaries = (getClosestPoint(points, self.boundaries[0]),
                                getClosestPoint(points, self.boundaries[1]))
        self.horizontal_boundaries = (getExtremePoint(points, False),
                                      getExtremePoint(points, True))
        self.vertical_boundaries = (getExtremePointLine(points, self.horizontal_boundaries, False),
                                    getExtremePointLine(points, self.horizontal_boundaries, True))
        self.ratio = calcRatio(self.boundaries)
        self.area = calcArea(self.boundaries)
        if self.area == 0:
            self.bg_prob = 0
        else:
            #FIXME: this should be calculated using the transformed image
            self.bg_prob = countOccur(pix, bg, self.boundaries) / float(self.area)


def brightness(im):
   stat = ImageStat.Stat(im)
   return stat.rms[0]



def colorAreas(image):
    black = tuple([0,0,0])
    white = tuple([255,255,255])

    xx, yy = image.size
    pix = image.load()

    ret = []

    for x in range(xx):
        for y in range(yy):
            if pix[x, y] == black:
                ret.append(Area(pix, (x, y), white, black, [[0, 0], [xx-1, yy-1]]))
    return ret




def ignoreAreas(image, areas, area_limits, ratio_limits, color_ratio_limits):
    pix = image.load()
    white = tuple([255,255,255])

    ret = []

    for area in areas:
        print (area.bg_prob)
        if inside([area.area], [[area_limits[0]], [area_limits[1]]]) and \
           inside([area.ratio], [[ratio_limits[0]], [ratio_limits[1]]]) and \
           inside([area.bg_prob], [[color_ratio_limits[0]], [color_ratio_limits[1]]]):
            ret.append(area);

    return ret

def drawHighlights(image, areas):
    draw = ImageDraw.Draw(image)
    for area in areas:
        p_min, p_max = area.boundaries
        draw.rectangle(list(p_min) + list(p_max), outline=tuple([0,128,128,128]))

        p_min, p_max = area.true_boundaries
        draw.rectangle(list(p_min) + list(p_max), outline=tuple([0, 255,0,128]))

        p_min, p_max = area.horizontal_boundaries
        draw.rectangle(list(p_min) + list(p_max), outline=tuple([0,0,255,128]))

        p_min_v, p_max_v = area.vertical_boundaries
        draw.polygon((p_min, p_min_v, p_max, p_max_v, p_min), outline=tuple([255,0,255,128]))


def main(filename):
    image_orig = Image.open(filename)
#    image_orig.show()
    image = image_orig.convert('L')


    # FIXME: 2/3 by trial and error
    threshold = brightness(image) * 2 / 3
    if threshold > 128:
        image = image.point(lambda p: p > threshold and 255)
    else:
        image = image.point(lambda p: p < threshold and 255)
    image = image.convert('RGB')

    # find connected areas
    areas = colorAreas(image)
    image.show()

    # find relevant connected areas
    size_min = 0.01 * image.size[0] * image.size[1]
    size_max = 0.7 * image.size[0] * image.size[1]
    areas = ignoreAreas(image,
                        areas,
                        [size_min, size_max],
                        [0.5, 1],
                        [0.1, 0.9])
    #    image.show()
    image = image_orig.copy().convert('RGBA')
    drawHighlights(image, areas)
    image.show()


if len(sys.argv) != 2:
    print "Usage: " + sys.argv[0] + " <filename>"
else:
    main(sys.argv[1])
