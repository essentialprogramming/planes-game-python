import random

from constants import Constants
from services.ServiceException import ServiceException
from domain.Plane import Plane
from utils.BoardUtils import BoardUtils
from utils.Collections import Collections
from utils.Matrix import Matrix
from utils.NumberUtils import NumberUtils


class GameService:

    def __init__(self, player, computer, difficulty):
        self.__player = player
        self.__computer = computer
        self.__difficulty = difficulty

        self.__turn = Constants.PLAYER

    @property
    def currentPlayer(self):
        return self.__player if self.__turn == Constants.PLAYER else self.__computer

    @property
    def nextPlayer(self):
        return self.__player if self.__turn == Constants.COMPUTER else self.__computer

    def placePlane(self, start_position, direction):
        strategyBoard = self.currentPlayer.getStrategyBoard()
        board = BoardUtils.clone(strategyBoard.getBoard())

        startPositionCoordinates = list(start_position)
        startPositionCoordinates = Collections.split(startPositionCoordinates, 2)[0]
        if len(startPositionCoordinates) != 2:
            raise ServiceException("Start position invalid, you can use for example: 'B4'.")

        position_row, position_column = map(str, startPositionCoordinates)

        row = NumberUtils.ordinal(position_row)
        column = int(position_column) - 1

        Matrix.checkIsInRange(board, row, column)

        board, plane_coordinates = GameService.insertPlane(board, row, column, direction)
        strategyBoard.setBoard(board)

        self.currentPlayer.setStrategyBoard(strategyBoard)
        self.currentPlayer.addPlaneCoordinates(plane_coordinates)

    def placeOpponentPlane(self):
        planesInserted = False
        while not planesInserted:
            self.resetPlayerBoard()
            strategyBoard = self.currentPlayer.getStrategyBoard()
            try:
                for plane_index in range(2):
                    rowIndex, columnIndex = BoardUtils.randomPosition(strategyBoard.getBoard())
                    row = NumberUtils.letter(rowIndex)
                    column = columnIndex + 1
                    startPosition = [row, column]
                    direction = random.sample(["up", "down", "left", "right"], 1)[0]
                    self.placePlane(startPosition, direction)
                planesInserted = True
            except ServiceException:
                continue
        self.nextTurn()

    @staticmethod
    def insertPlane(board, row, column, direction):
        cabinRow, cabinColumn = None, None
        plane = Plane.createPlaneMatrix()
        if direction == "left":
            plane = Matrix.rotateRight(plane)
            cabinRow, cabinColumn = 2, 3
        elif direction == "right":
            plane = Matrix.rotateLeft(plane)
            cabinRow, cabinColumn = 2, 0
        elif direction == "up":
            plane = Matrix.rotate180(plane)
            cabinRow, cabinColumn = 3, 2
        elif direction == "down":
            cabinRow, cabinColumn = 0, 2

        GameService.validatePosition(board, plane, row, column, cabinRow, cabinColumn)
        Matrix.insertMatrixAtPosition(board, plane, row, column, cabinRow, cabinColumn)

        return board, Matrix.getCoordinates(board, plane, row, column, cabinRow, cabinColumn)

    @staticmethod
    def validatePosition(board, plane, row, column, rowInSubMatrix, columnInSubMatrix):
        position_error = ServiceException("There's not enough space to draw a plane given this start position and "
                                             "direction.")
        overlap_error = ServiceException("The planes cannot overlap ")
        if not Matrix.fitsInGrid(board, plane, row, column, rowInSubMatrix, columnInSubMatrix):
            raise position_error
        if Matrix.isOverlapping(board, plane, row, column, rowInSubMatrix, columnInSubMatrix):
            raise overlap_error

    def strikeBoard(self, strikePosition):
        position_row, position_column = map(str, strikePosition)
        row, column = NumberUtils.ordinal(position_row), int(position_column) - 1

        strikeBoard = self.nextPlayer.getStrategyBoard().getBoard()
        targetBoard = self.currentPlayer.getTargetBoard().getBoard()

        Matrix.checkIsInRange(strikeBoard, row, column)

        strikePosition = strikeBoard[row][column]

        if strikePosition == 'O' or strikePosition == 'X' or strikePosition == 'D':
            raise ServiceException("This position has already been hit.")

        if strikePosition == ' ':
            targetBoard[row][column] = strikeBoard[row][column] = 'O'
        elif strikePosition == 'T' or strikePosition == 'W':
            targetBoard[row][column] = strikeBoard[row][column] = 'X'
        elif strikePosition == 'H':
            targetBoard[row][column] = strikeBoard[row][column] = 'D'
            if self.__difficulty == "medium":
                plane_coordinates = self.nextPlayer.getPlaneCoordinates(row=row, column=column)
                for row, column in plane_coordinates:
                    targetBoard[row][column] = strikeBoard[row][column] = 'X'

    def computerStrikeBoard(self):
        boardIsHit = False
        while not boardIsHit:
            try:
                targetBoard = self.currentPlayer.getTargetBoard()
                hitBoard = self.nextPlayer.getStrategyBoard()
                boardHits = self.getBoardHits(hitBoard)
                if len(boardHits) == 0:
                    rowIndex, columnIndex = BoardUtils.randomPosition(targetBoard.getBoard())
                    plane_row = NumberUtils.letter(rowIndex)
                    plane_column = columnIndex + 1
                else:
                    random_hit = random.sample(boardHits, 1)[0]
                    rowIndex, columnIndex = BoardUtils.randomEmptyNeighbour(targetBoard.getBoard(), random_hit[0], random_hit[1])
                    plane_row = NumberUtils.letter(rowIndex)
                    plane_column = columnIndex + 1
                strike_position = [plane_row, plane_column]
                self.strikeBoard(strike_position)
                print('AI struck position: ' + plane_row + str(plane_column))
                boardIsHit = True
            except ServiceException:
                continue
        self.nextTurn()

    def getBoardHits(self, targetBoard):
        board = targetBoard.getBoard()
        board_hits = []
        for row in range(len(board)):
            line = board[row]
            for column in range(len(line)):
                if board[row][column] == 'X' and self.inAlivePlane(row, column, board):
                    board_hits.append([row, column])
        return board_hits

    def inAlivePlane(self, x, y, board):
        for plane in self.nextPlayer.getPlanes():
            for row, column in plane.getCoordinates():
                if board[row][column] == 'H':
                    if (x, y) in plane.getCoordinates():
                        return True
        return False

    def nextTurn(self):
        self.__turn = 1 if self.__turn == 2 else 2

    def getPlayer(self):
        return self.currentPlayer

    def getNextPlayer(self):
        return self.nextPlayer

    def getPlayerPlanesCount(self):
        board = self.currentPlayer.getStrategyBoard().getBoard()
        return self.alivePlanesCount(board)

    def getOpponentPlanesCount(self):
        board = self.nextPlayer.getStrategyBoard().getBoard()
        return self.alivePlanesCount(board)

    @staticmethod
    def alivePlanesCount(board):
        return BoardUtils.count(board, 'H')

    def resetPlayerBoard(self):
        self.currentPlayer.reset()
