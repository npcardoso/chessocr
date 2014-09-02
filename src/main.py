import sys
from area import Area
from floodfill import inside
from PIL import Image, ImageFilter, ImageStat, ImageDraw

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


def ignoreAreas(image, areas, area_limits, ratio_limits):
    pix = image.load()
    white = tuple([255,255,255])

    ret = []

    for area in areas:
        if inside([area.area], [[area_limits[0]], [area_limits[1]]]) and \
           inside([area.ratio], [[ratio_limits[0]], [ratio_limits[1]]]):
            ret.append(area);

    return ret







def main(filename):
    image_orig = Image.open(filename)
#    image_orig.show()

# to grayscale
    image = image_orig.convert('L')
#    image.show()


# to black and white
# FIXME: 2/3 by trial and error
    threshold = brightness(image) * 2 / 3
    if threshold > 128:
        image = image.point(lambda p: p > threshold and 255)
    else:
        image = image.point(lambda p: p < threshold and 255)
    image = image.convert('RGB')
#    image.show()

# find connected areas
    areas = colorAreas(image)

# find relevant connected areas
    size_min = 0.01 * image.size[0] * image.size[1]
    size_max = 0.7 * image.size[0] * image.size[1]
    areas = ignoreAreas(image,
                        areas,
                        [size_min, size_max],
                        [0.5, 1])
#    image.show()

#    image = image_orig.copy().convert('RGBA')
#    draw = ImageDraw.Draw(image)
#    for area in areas:
#        area.drawHighlights(draw)
#    image.show()

    image = image_orig.copy().convert('RGBA')
    for a in areas:
        tmp = a.extractArea(image, 1024, 1024);
        tmp.show()

if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " <filename>")
else:
    main(sys.argv[1])
