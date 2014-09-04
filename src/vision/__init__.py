import cv2
import numpy as np
import random

from vision.floodfill import inside


from area import Area

def getAreas(image):
    im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    im_bw = cv2.cvtColor(im_bw, cv2.COLOR_GRAY2BGR)
    black = (0, 0, 0,)

    yy, xx, _ = image.shape
    ret = []

    mask = np.zeros((yy + 2, xx + 2), np.uint8)
    for x in range(xx):
        for y in range(yy):
            if all(im_bw[y,x] == black):
                color = (1 + x % 254,
                         1 + y % 254,
                         random.randint(1,255))

                print "started floodfill @ ", (x,y)
                pixels, props = cv2.floodFill(im_bw, mask, (x, y), color, flags = 8)
                print "finished floodfill"
                ret.append(Area(color, pixels, props[0:2], props[2:4], (x,y)))
    return (im_bw, ret)


def ignoreAreas(areas, area_limits, ratio_limits):
    white = tuple([255, 255, 255])

    ret = []

    for area in areas:
        if inside([area.getArea()], [[area_limits[0]], [area_limits[1]]]) and \
           inside([area.getRatio()], [[ratio_limits[0]], [ratio_limits[1]]]):
           ret.append(area)

    return ret
