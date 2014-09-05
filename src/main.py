import sys
sys.path.append('/usr/lib/python2.7/site-packages/')
sys.path.append('/usr/local/lib/python2.7/site-packages/')

from util import showImage, drawPerspective, drawBoundaries, drawLines, drawPoint, extractPerspective
from extract import extractBoards, extractGrid
import cv2

from line import Line


extract_width=400
extract_height=400


def main(filename):
   image = cv2.imread(filename)

   boards = extractBoards(image, extract_width, extract_height)
   for b in boards:
      horizontal, vertical = extractGrid(b, 9, 9)
      b = b.copy()
      drawLines(b, horizontal)
      drawLines(b, vertical, color=(255,0,0))
      for h in horizontal:
         for v in vertical:
            drawPoint(b, h.intersect(v), (0,255,255))
      showImage(b)





if len(sys.argv) < 2 or len(sys.argv) > 3:
   print("Usage: " + sys.argv[0] + " <filename> [<threshold_adj>]")
elif len(sys.argv) == 2:
   main(sys.argv[1])
elif len(sys.argv) == 3:
   main(sys.argv[1], float(sys.argv[2]))
