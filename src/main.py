import sys
sys.path.append('/usr/lib/python2.7/site-packages/')
sys.path.append('/usr/local/lib/python2.7/site-packages/')

from board import Board
from extract import extractBoards, extractGrid, extractTiles, ignoreContours, largestContour
from util import showImage, drawPerspective, drawBoundaries, drawLines, drawPoint, drawContour, extractPerspective, randomColor
import random
import cv2
import numpy as np

from line import Line


extract_width=400
extract_height=400


def extractPiece(tile, margin=0.05):
   imgs = [tile]
   w, h, _ = tile.shape

   im_gray = cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY)
   imgs.append(cv2.cvtColor(im_gray, cv2.COLOR_GRAY2BGR))

#   im_gray = im_gray[(h*margin):(h*(1-margin)),
#                     (w*margin):(w*(1-margin))]
#   imgs.append(cv2.cvtColor(im_gray, cv2.COLOR_GRAY2BGR))


#   im_gray = cv2.equalizeHist(im_gray)
   im_gray = cv2.medianBlur(im_gray, 3)
   imgs.append(cv2.cvtColor(im_gray, cv2.COLOR_GRAY2BGR))



   bright = np.mean(im_gray)
   im_bw = im_gray
   im_bw[np.where(im_gray < bright)] = 0
   im_bw[np.where(im_gray >= bright)] = 255
   imgs.append(cv2.cvtColor(im_bw, cv2.COLOR_GRAY2BGR))


   if np.mean(im_bw) < 128:
      im_bw = 255 - im_bw

   imgs.append(cv2.cvtColor(im_bw, cv2.COLOR_GRAY2BGR))


   #_, im_bw = cv2.threshold(im_gray, 50, 250, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
   #im_bw = cv2.Canny(im_bw, 0,255, apertureSize=5)



   contours,hierarchy = cv2.findContours(im_bw.copy(),  cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)

   hulls = [cv2.convexHull(c) for c in contours]
   ids = ignoreContours(im_bw, hulls, max_area_percentage=0.75, min_area_percentage=0.2)

   im_bw = cv2.cvtColor(im_bw, cv2.COLOR_GRAY2BGR)
   tmp = im_bw.copy()
   for i in ids:
      c = np.squeeze(hulls[i], 1)
      drawContour(tmp, c, randomColor(), thickness=1)

   imgs.append(tmp)

   showImage(np.hstack(imgs))





def main(filename, extractB=False):
   image = cv2.imread(filename)

   if extractB:
      print("Extracting Boards")
      boards = extractBoards(image, extract_width, extract_height)
   else:
      boards = [image]

   for b in boards:
      print("Extracting Grid")
      grid = (horizontal, vertical) = extractGrid(b, 9, 9)
      print grid
      print("Extracting Tiles")
      b = Board(extractTiles(b, grid, 100, 100), 8, 8)
      #drawLines(b, horizontal)
      #drawLines(b, vertical, color=(255,0,0))
      #for h in horizontal:
      #   for v in vertical:
      #      drawPoint(b, h.intersect(v), (0,255,255))
      board_id = int(random.randint(0, 100000))
      for x in range(8):
         for y in (0,1, 6,7):
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
