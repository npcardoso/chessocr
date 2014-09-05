import cv2
import numpy as np


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

def filterCloseLines(lines, horizontal=True, threshold = 40):
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
