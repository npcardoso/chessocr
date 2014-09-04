import sys
sys.path.append('/usr/lib/python2.7/site-packages/')
sys.path.append('/usr/local/lib/python2.7/site-packages/')

from util import showImage, drawPerspective, drawBoundaries, extractPerspective
from vision import getAreas, ignoreAreas

import cv2


extract_width=400
extract_height=400


def main(filename):
   image = cv2.imread(filename)
   #find connected areas
   im_areas, areas = getAreas(image.copy())

   # find relevant connected areas
   size_min = 0.02 * image.shape[0] * image.shape[1]
   size_max = 0.7 * image.shape[0] * image.shape[1]
   areas = ignoreAreas(areas, [size_min, size_max], [0.5, 1])

   boards = []
   for area in areas:
      perspective = area.getPerspective(im_areas)
      b = extractPerspective(image, perspective, extract_width, extract_height)
      boards.append(b)

      im_tmp = im_areas.copy()
      drawPerspective(im_tmp, perspective)
      drawBoundaries(im_tmp, area.getBoundaries(), area.getColor())
      #      showImage(im_tmp)

   for b in boards:
      showImage(b)



if len(sys.argv) < 2 or len(sys.argv) > 3:
   print("Usage: " + sys.argv[0] + " <filename> [<threshold_adj>]")
elif len(sys.argv) == 2:
   main(sys.argv[1])
elif len(sys.argv) == 3:
   main(sys.argv[1], float(sys.argv[2]))
