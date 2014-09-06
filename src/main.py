import sys
sys.path.append('/usr/lib/python2.7/site-packages/')
sys.path.append('/usr/local/lib/python2.7/site-packages/')

from board import Board
from extract import extractBoards, extractGrid, extractTiles, ignoreContours
from util import showImage, drawPerspective, drawBoundaries, drawLines, drawPoint, drawContour, extractPerspective, randomColor
import random
import cv2
import numpy as np

from line import Line


extract_width=400
extract_height=400


def extractPiece(tile):
   im_gray = cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY)
   (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
   contours,hierarchy = cv2.findContours(im_bw,  cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
   contour_ids = ignoreContours(im_bw, contours, hierarchy, min_area_percentage=0.3)
   c = []
   for i in contour_ids:
      c = contours[i]
      c = np.squeeze(c,1)

      drawContour(tile, c, randomColor(), thickness=1)
   if len(c):
      showImage(tile)




def main(filename, extractB=False):
   image = cv2.imread(filename)

   if extractB:
      boards = extractBoards(image, extract_width, extract_height)
   else:
      boards = [image]

   print extractB, boards
   for b in boards:
      grid = (horizontal, vertical) = extractGrid(b, 9, 9)
      b = Board(extractTiles(b, grid, 50, 50), 8, 8)
      #drawLines(b, horizontal)
      #drawLines(b, vertical, color=(255,0,0))
      #for h in horizontal:
      #   for v in vertical:
      #      drawPoint(b, h.intersect(v), (0,255,255))
      board_id = int(random.randint(0, 100000))
      for x in range(8):
         for y in range(8):
            t = b.getTile(x,y)
            print "Checking tile ", t.getX(), t.getY()
            extractPiece(t.getImage())
#            cv2.imwrite("extracted_tiles/Board-%d - (%d,%d).png" % (board_id, t.getX(), t.getY()), t.getImage())





if len(sys.argv) < 2 or len(sys.argv) > 3:
   print("Usage: " + sys.argv[0] + " <filename> [<extractBoards?>]")
elif len(sys.argv) == 2:
   main(sys.argv[1])
elif len(sys.argv) == 3:
   main(sys.argv[1], bool(sys.argv[2]))
