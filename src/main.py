import sys
sys.path.append('/usr/lib/python2.7/site-packages/')
sys.path.append('/usr/local/lib/python2.7/site-packages/')

from board import Board
from extract import extractBoards, extractGrid, extractTiles, ignoreContours, largestContour
from util import showImage, drawPerspective, drawBoundaries, drawLines, drawPoint, drawContour, randomColor
from line import Line

import random
import cv2
import numpy as np
import argparse



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


   return imgs





def main_dev(board, args):
   pass

def main_train(board, args):
   pass

def main_show_tiles(board, args):
   imgs = []
   for y in range(8):
      imgs_row = []
      for x in range(8):
         t = board.getTile(x,y)
         tmp = extractPiece(t.getImage())
         imgs_row.append(np.vstack(tmp))
      imgs.append(np.hstack(imgs_row))

   showImage(np.vstack(imgs))






def main(argv):
   actions = {}
   actions["train"] = main_train
   actions["show_tiles"] = main_show_tiles
   actions["dev"] = main_dev


   parser = argparse.ArgumentParser(description='A chess OCR application.')
   parser.add_argument('filenames', metavar='filename', type=str, nargs='+',
                       help='The files to process.')

   parser.add_argument('-e', dest='extract_boards', action='store_const',
                       const=True, default=False,
                       help='extract boards from images (default: use image as-is)')

   parser.add_argument('-a', dest='action', default="show_tiles",
                       choices=["train", "show_tiles", "dev"],
                       help='action to perform (default: show_tiles)')

   args = parser.parse_args()

   action = actions[args.action]



   for filename in args.filenames:
      image = cv2.imread(filename)
      print("---- %s ----" % filename)

      if args.extract_boards:
         print("Extracting Boards")
         boards = extractBoards(image, extract_width, extract_height)
      else:
         boards = [image]

      for b in boards:
         print("Extracting Grid")
         grid = extractGrid(b, 9, 9)

         print(grid)
         if grid is None:
            print("Could not find Grid")
            continue

         print("Extracting Tiles")
         tiles = extractTiles(b, grid, 100, 100)

         b = Board(tiles, 8, 8)

         print("Running action")
         action(b, args)



main(sys.argv)
