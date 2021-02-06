from domain.Board import Board
from domain.Plane import Plane


class Player:

    def __init__(self):
        self.strategyBoard = Board()
        self.targetBoard = Board()
        self.numberOfPlanes = 0
        self.planes = []

    def getStrategyBoard(self):
        return self.strategyBoard

    def setStrategyBoard(self, strategyBoard=None):
        if strategyBoard is None:
            strategyBoard = Board()
        self.strategyBoard = strategyBoard

    def getTargetBoard(self):
        return self.targetBoard

    def setTargetBoard(self, targetBoard=None):
        if targetBoard is None:
            targetBoard = Board()
        self.targetBoard = targetBoard

    def getPlaneCoordinates(self, row, column):
        for plane in self.planes:
            for rowIndex, columnIndex in plane.getCoordinates():
                if rowIndex == row and columnIndex == column:
                    return plane.getCoordinates()

    def addPlaneCoordinates(self, plane_coordinates):
        plane = Plane()
        plane.addCoordinates(plane_coordinates)
        self.planes.append(plane)
        self.numberOfPlanes += 1

    def getPlanes(self):
        return self.planes

    def getNumberOfPlanes(self):
        return self.numberOfPlanes

    def reset(self):
        self.targetBoard = Board()
        self.strategyBoard = Board()
        self.planes.clear()
        self.numberOfPlanes = 0
