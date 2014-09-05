import sys
sys.path.append('/usr/lib/python2.7/site-packages/')
sys.path.append('/usr/local/lib/python2.7/site-packages/')

from util import showImage, drawPerspective, drawBoundaries, extractPerspective
from extract import extractBoards

import cv2


extract_width=400
extract_height=400


def main(filename):
   image = cv2.imread(filename)
   #find connected areas

   boards = extractBoards(image, extract_width, extract_height)
   for b in boards:
      showImage(b)



if len(sys.argv) < 2 or len(sys.argv) > 3:
   print("Usage: " + sys.argv[0] + " <filename> [<threshold_adj>]")
elif len(sys.argv) == 2:
   main(sys.argv[1])
elif len(sys.argv) == 3:
   main(sys.argv[1], float(sys.argv[2]))
