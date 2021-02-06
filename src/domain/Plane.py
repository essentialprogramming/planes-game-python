from constants import Constants
from utils.BoardUtils import BoardUtils


class Plane(object):
    """description of class"""

    def __init__(self, cabinLocation=None, tailDirection=None):
        self.cabinLocation = cabinLocation
        self.tailDirection = tailDirection
        self.__plane = self.createPlaneMatrix()
        self.planeCoordinates = []

    def getCabinLocation(self):
        return self.cabinLocation

    def getTailDirection(self):
        return self.tailDirection

    @staticmethod
    def createPlaneMatrix():
        """
        Creates the plane matrix for the up direction if it is another direction it will just rotate the matix
        What the matrix has to look like
        0 0 1 0 0
        1 1 1 1 1
        0 0 1 0 0
        0 1 1 1 0
        """
        plane_matrix = BoardUtils.createBoard(Constants.EMPTY, 4, 5)
        plane_matrix[0][2] = 'H'
        for index in range(0, 5):
            plane_matrix[1][index] = 'W'
        for index in range(1, 4):
            plane_matrix[3][index] = 'W'
        plane_matrix[1][2] = 'T'
        plane_matrix[2][2] = 'T'
        plane_matrix[3][2] = 'T'
        return plane_matrix

    def addCoordinates(self, planeCoordinates):
        self.planeCoordinates.clear()
        self.planeCoordinates.extend(planeCoordinates)

    def getCoordinates(self):
        return self.planeCoordinates

    def __eq__(self, location):
        if self.cabinLocation[0] == location[0] and self.cabinLocation[1] == location[1]:
            return True
        else:
            return False
