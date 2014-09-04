import cv2
import numpy as np

def showImage(image, name="image"):
    print("Showing image: '%s'" % name)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def drawBoundaries (image, boundaries, color=(128, 128, 0)):
    p_min, p_max = boundaries
    cv2.rectangle(image, p_min, p_max, color)


def drawPerspective(image, perspective):
    (a,b,c,d) = perspective
#    cv2.polylines(image, np.array(perspective, 'int32'), False, (0,0,255))
    cv2.line(image, a, c, (255,0,0))
    cv2.line(image, b,d, (255, 0, 255))


def extractPerspective(image, perspective, w, h, dest=None):
    if dest is None:
        dest = ((0,0), (w, 0), (w,h), (0, h))

    perspective = np.array(perspective ,np.float32)
    dest = np.array(dest ,np.float32)

    coeffs = cv2.getPerspectiveTransform(perspective, dest)
    return cv2.warpPerspective(image, coeffs, (w, h))
