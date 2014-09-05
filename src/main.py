import sys
sys.path.append('/usr/lib/python2.7/site-packages/')
sys.path.append('/usr/local/lib/python2.7/site-packages/')

from board import Board
from extract import extractBoards, extractGrid, extractTiles
from util import showImage, drawPerspective, drawBoundaries, drawLines, drawPoint, extractPerspective

import cv2

from line import Line


extract_width=400
extract_height=400


def main(filename):
   image = cv2.imread(filename)

   boards = extractBoards(image, extract_width, extract_height)
   for b in boards:
      grid = (horizontal, vertical) = extractGrid(b, 9, 9)
      b = Board(extractTiles(b, grid, 50, 50), 8, 8)

      #drawLines(b, horizontal)
      #drawLines(b, vertical, color=(255,0,0))
      #for h in horizontal:
      #   for v in vertical:
      #      drawPoint(b, h.intersect(v), (0,255,255))
      for x in range(8):
         for y in range(8):
            t = b.getTile(x,y)
            showImage(t.getImage(), name = "Tile: (%d,%d)" % (t.getX(), t.getY()))





if len(sys.argv) < 2 or len(sys.argv) > 3:
   print("Usage: " + sys.argv[0] + " <filename> [<threshold_adj>]")
elif len(sys.argv) == 2:
   main(sys.argv[1])
elif len(sys.argv) == 3:
   main(sys.argv[1], float(sys.argv[2]))
