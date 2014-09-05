import cv2
import numpy as np
from util import showImage, drawPerspective, drawBoundaries, drawContour
from line import Line, partitionLines, filterCloseLines


houghThreshold = 150

def getPerspective(image, points):
    yy, xx, _ = image.shape
    tmp = np.zeros(image.shape[0:2], np.uint8);
    drawContour(tmp, points, (255,), 1)
    showImage(tmp)

    grid = None
    for i in range(houghThreshold):
        lines = cv2.HoughLines(tmp, 1, np.pi / 180, houghThreshold-i)
        if lines is None:
            continue
        lines = [Line(l[0], l[1]) for l in lines[0]]
        (vertical, horizontal) = partitionLines(lines)
        vertical = filterCloseLines(vertical, horizontal=False)
        horizontal = filterCloseLines(horizontal, horizontal=True)

        if len(vertical) == 2 and len(horizontal) == 2:
            grid = (vertical, horizontal)
            break


    if grid is None:
        return None


    if vertical[0].center[0] > vertical[1].center[0]:
        v2, v1 = vertical
    else:
        v1, v2 = vertical

    if horizontal[0].center[1] > horizontal[1].center[1]:
        h2, h1 = horizontal
    else:
        h1, h2 = horizontal



    perspective = (h1.intersect(v1),
                   h1.intersect(v2),
                   h2.intersect(v2),
                   h2.intersect(v1))
    return perspective
