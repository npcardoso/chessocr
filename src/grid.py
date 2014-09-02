import sys

# FIXME: needed on arch..
sys.path.append('/usr/lib/python2.7/site-packages/')

import cv2
import numpy as np

threshold1 = 50
threshold2 = 150
apertureSize = 3

houghThreshold = 200
thresholdDecr = 5

gridWidth = 640
gridHeight = 640
closeLineThreshold = 40

class Line:
    def __init__(self, rho, theta):
        self.rho = rho
        self.theta = theta
        self.cos_factor = np.cos(theta)
        self.sin_factor = np.sin(theta)
        self.center = (self.cos_factor * rho, self.sin_factor * rho)


    def getSegment(self, lenLeft, lenRight):
        a = self.cos_factor
        b = self.sin_factor
        (x0, y0) = self.center

        x1 = int(x0 + lenRight * (-b))
        y1 = int(y0 + lenRight * a)
        x2 = int(x0 - lenLeft * (-b))
        y2 = int(y0 - lenLeft  * a)
        return ((x1, y1), (x2, y2))

    def isHorizontal(self, thresholdAngle=np.pi / 4):
        return abs(np.cos(self.theta)) < np.cos(thresholdAngle)

    def isVertical(self, thresholdAngle=np.pi / 4):
        return abs(np.sin(self.theta)) < np.cos(thresholdAngle)

    def intersect(self, line):
        ct1 = np.cos(self.theta)
        st1 = np.sin(self.theta)
        ct2 = np.cos(line.theta)
        st2 = np.sin(line.theta)
        d = ct1 * st2 - st1 * ct2
        if d == 0.0: raise ValueError('parallel lines')
        x = (st2 * self.rho - st1 * line.rho) / d
        y = (-ct2 * self.rho + ct1 * line.rho) / d
        return (x, y)

    def draw(self, image, color=(0,0,255)):
        p1, p2 = self.getSegment(1000,1000)
        cv2.line(image, p1, p2, color, 2)


def partitionLines(lines):
    h = filter(lambda x: x.isHorizontal(), lines)
    v = filter(lambda x: x.isVertical(), lines)

    h = [(l.center[1], l) for l in h]
    v = [(l.center[0], l) for l in v]

    h.sort()
    v.sort()

    h = [l[1] for l in h]
    v = [l[1] for l in v]

    return (v, h)

def filterCloseLines(lines, horizontal=True, threshold = closeLineThreshold):
    if horizontal:
        item = 1
    else:
        item = 0

    i = 0
    ret = []
    while i < len(lines):
        itmp = i
        while i < len(lines) and (lines[i].center[item] - lines[itmp].center[item] < threshold):
            i += 1
        target = int(itmp + ((i-itmp) / 2))
        ret.append(lines[target])
    return ret

def drawLines(image, lines):
    for l in lines:
        l.draw(image)

def drawPoint(image, point):
    cv2.circle(image, point, 10, (0, 0, 255), -1)

def grid(filename):
    im_gray = cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    resized_im = cv2.resize(im_gray, (gridWidth, gridHeight))
    (thresh, im_bw) = cv2.threshold(resized_im, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    print("threshold: " + str(thresh))
    edges = cv2.Canny(im_bw, threshold1, threshold2, apertureSize = apertureSize)
    bgr = cv2.cvtColor(im_bw, cv2.COLOR_GRAY2BGR)

    for i in range(houghThreshold / thresholdDecr):
        lines = cv2.HoughLines(edges, 1, np.pi / 180, houghThreshold - (i * thresholdDecr))
        if lines is None:
            continue

        lines = [Line(l[0], l[1]) for l in lines[0]]
        (vertical, horizontal) = partitionLines(lines)
        vertical = filterCloseLines(vertical, horizontal=False)
        horizontal = filterCloseLines(horizontal, horizontal=True)

        if len(vertical) >= 8 and len(horizontal) >= 8: break

    bgr = cv2.cvtColor(resized_im, cv2.COLOR_GRAY2BGR)
    drawLines(bgr, horizontal)
    drawLines(bgr, vertical)

    for h in horizontal:
        for v in vertical:
            drawPoint(bgr, h.intersect(v))

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', bgr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " <filename>")
else:
    grid(sys.argv[1])
