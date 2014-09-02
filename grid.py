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

def point(rho, theta):
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * a)
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * a)
    return [(x1, y1), (x2, y2)]

def horizontal(theta):
    return abs(np.cos(theta)) < np.cos(np.pi / 4)

def vertical(theta):
    return not horizontal(theta)

def partitionLines(lines):
    def map1(x):
        ((x1, y1), (x2, y2)) = point(x[0], x[1])
        return (x1 + x2) / 2
    def map2(x):
        ((x1, y1), (x2, y2)) = point(x[0], x[1])
        return (y1 + y2) / 2

    v = map(map1, filter(lambda x: vertical(x[1]), lines))
    v.sort()
    h = map(map2, filter(lambda x: horizontal(x[1]), lines))
    h.sort()

    return (v, h)

def filterCloseLines(lines, threshold = closeLineThreshold):
    i = 0
    ret = []
    while i < len(lines):
        itmp = i
        cnt = 0
        while i < len(lines) and (lines[i] - lines[itmp] < threshold):
            cnt += lines[i]
            i += 1
        ret.append(cnt / (i - itmp))

    return ret

def drawLines(image, horizontal, vertical):
    for x in vertical:
        cv2.line(image, (x, 0), (x, 1000), (0, 0, 255), 2)
    for y in horizontal:
        cv2.line(image, (0, y), (1000, y), (0, 0, 255), 2)

def grid(filename):
    im_gray = cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    resized_im = cv2.resize(im_gray, (gridWidth, gridHeight))
    (thresh, im_bw) = cv2.threshold(resized_im, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    print "threshold: " + str(thresh)
    edges = cv2.Canny(im_bw, threshold1, threshold2, apertureSize = apertureSize)
    bgr = cv2.cvtColor(im_bw, cv2.COLOR_GRAY2BGR)

    for i in range(houghThreshold / thresholdDecr):
        lines = cv2.HoughLines(edges, 1, np.pi / 180, houghThreshold - (i * thresholdDecr))
        if lines is None:
            continue

        lines = lines[0]
        (vertical, horizontal) = partitionLines(lines)
        vertical = filterCloseLines(vertical)
        horizontal = filterCloseLines(horizontal)

        if len(vertical) >= 8 and len(horizontal) >= 8: break

    drawLines(bgr, horizontal, vertical)

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', bgr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

grid('examples/board1.jpg')
# grid('examples/board2.jpg')
# grid('examples/board3.jpg')
# grid('examples/board4.jpg')
