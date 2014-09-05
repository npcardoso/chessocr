import sys

# FIXME: needed on arch..
sys.path.append('/usr/lib/python2.7/site-packages/')
sys.path.append('/usr/local/lib/python2.7/site-packages/')

import cv2
import numpy as np

from line import Line, partitionLines, filterCloseLines

threshold1 = 50
threshold2 = 150
apertureSize = 3

houghThreshold = 200
thresholdDecr = 5

gridWidth = 640
gridHeight = 640





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
