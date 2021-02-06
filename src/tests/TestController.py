import unittest

from domain.Plane import Plane
from utils.BoardUtils import BoardUtils
from utils.Matrix import Matrix
from utils.Utils import Utils
from services.GameService import GameService
from constants import Constants


class TestController(unittest.TestCase):

    @staticmethod
    def matrix_operations():
        plane = Plane.createPlaneMatrix()

        BoardUtils.printBoardV3(plane, Matrix.rotate180(plane))
        BoardUtils.printBoardV3(Matrix.rotateLeft(plane), Matrix.rotateRight(plane))

    def testAll(self):
        self.matrix_operations()


if __name__ == '__main__':
    unittest.main()
