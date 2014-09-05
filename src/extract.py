from perspective import getPerspective
from util import ratio, extractPerspective
from util import showImage, drawPerspective, drawBoundaries, drawContour


import cv2
import numpy as np


def ignoreContours(img,
                   contours,
                   hierarchy,
                   min_ratio_bounding=0.6,
                   min_area_percentage=0.01,
                   max_area_percentage=0.40,
                   min_ratio_rect=0.5):
    ret = []
    i = -1

    img_area = img.shape[0] * img.shape[1]

    for c in contours:
        i += 1

        if not hierarchy[i][2] == -1:
            continue

        _,_,w,h = tmp = cv2.boundingRect(c)
        if ratio(h,w) < min_ratio_bounding:
            continue

        contour_area = cv2.contourArea(c)
        img_contour_ratio = ratio(img_area, contour_area)
        if img_contour_ratio < min_area_percentage:
            continue
        if img_contour_ratio > max_area_percentage:
            continue

        ret.append(i)

    return ret


def extractBoards(img, w, h):
   im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
   im_gray = cv2.cvtColor(im_gray, cv2.COLOR_GRAY2BGR)

   contours,hierarchy = cv2.findContours(im_bw,  cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)
   hierarchy = np.squeeze(hierarchy)

   contour_ids = ignoreContours(im_bw, contours, hierarchy)

   boards = [im_gray]

   for i in contour_ids:
       color = (0,0,255)
       c = contours[i]

       hull = cv2.convexHull(contours[i])
       hull = np.squeeze(hull,1)

       drawContour(im_gray, hull, color)
       perspective=getPerspective(img, hull)

       if perspective is not None:
           b = extractPerspective(img, perspective, w, h)
           boards.append(b)
           drawPerspective(im_gray, perspective)

   return boards
