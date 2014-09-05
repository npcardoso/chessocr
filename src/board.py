import cv2
import numpy as np

from util import ratio


class Board:
    def __init__(self, tiles, w, h):
        self._board = [None] * w * h
        self._w = w
        self._h = h

        for (x,y), t in tiles:
            if self._isInsideBoard(x, y):
                self.setTile(x, y, t)

    def _isInsideBoard(self, x, y):
        return x < self._w and y < self._h and x >= 0 and y >= 0

    def _getBoardCellId(self, x, y):
        return self._w * y + x

    def setTile(self, x, y, t):
        assert(self._isInsideBoard(x, y))
        self._board[self._getBoardCellId(x,y)] = Tile(x, y, t)

    def getTile(self, x, y):
        assert(self._isInsideBoard(x, y))
        return self._board[self._getBoardCellId(x,y)]


class Tile:
    def __init__(self, x, y, image):
        self._x = x
        self._y = y
        self._image = image

    def getX(self):
        return self._x

    def getY(self):
        return self._y

    def getImage(self):
        return self._image
