import sys
sys.path.append('/usr/lib/python2.7/site-packages/')
sys.path.append('/usr/local/lib/python2.7/site-packages/')
from area import Area, showImage
from floodfill import inside
from PIL import Image, ImageFilter, ImageStat, ImageDraw
import cv2

def colorAreas(image):
    black = tuple([0, 0, 0])
    xx, yy, _ = image.shape
    ret = []

    i = 0
    for x in range(xx):
        for y in range(yy):
            print image[x, y]
            print image[x, y] == black
            print all(image[x, y] == black)
            if all(image[x, y] == black):
               i += 1
               ret.append(Area(image, (x, y)))
    print i
    return ret


def ignoreAreas(areas, area_limits, ratio_limits):
    white = tuple([255, 255, 255])

    ret = []

    for area in areas:
        if inside([area.area], [[area_limits[0]], [area_limits[1]]]) and \
           inside([area.ratio], [[ratio_limits[0]], [ratio_limits[1]]]):
           ret.append(area)

    return ret

def main(filename):
    im_color = cv2.imread(filename)
    im_gray = cv2.imread(filename, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    print("threshold: " + str(thresh))
    im_areas = cv2.cvtColor(im_bw, cv2.COLOR_GRAY2BGR)

    # showImage(im_color)
    # showImage(im_gray)
    # showImage(im_bw)
    # showImage(im_areas)

    # cv2.imshow("color", im_color)
    # cv2.imshow("gray", im_gray)

    # find connected areas
    areas = colorAreas(im_areas)

    # find relevant connected areas
    size_min = 0.01 * im_color.shape[0] * im_color.shape[1]
    size_max = 0.7 * im_color.shape[0] * im_color.shape[1]
    areas = ignoreAreas(areas,
                        [size_min, size_max],
                        [0.5, 1])
    # image.show()

    for area in areas:
        area.drawHighlights(im_color)
    cv2.imshow("image", im_color);

    # image = image_orig.copy().convert('RGBA')
    for a in areas:
        tmp = a.extractArea(image, 1024, 1024);
        cv2.imshow("image", tmp);

if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: " + sys.argv[0] + " <filename> [<threshold_adj>]")
elif len(sys.argv) == 2:
    main(sys.argv[1])
elif len(sys.argv) == 3:
    main(sys.argv[1], float(sys.argv[2]))
