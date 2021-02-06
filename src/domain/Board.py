from constants import Constants
from utils.BoardUtils import BoardUtils


class Board:

    def __init__(self):
        self.board = BoardUtils.createBoard(Constants.EMPTY, Constants.ROW_COUNT, Constants.COLUMN_COUNT)

    def getBoard(self):
        return self.board

    def setBoard(self, board):
        self.board = board
