from utils.BoardUtils import BoardUtils
from utils.Utils import Utils


class UI:

    def __init__(self, gameController):
        self.controller = gameController

        self.MENU = {
            1: "1. Draw planes",
            2: "2. Retry",
            3: "3. Start game",
            4: "4. Exit"
        }

        """
        A dictionary containing references to
        certain functions based on user input
        """
        self.commandsDictionary = {
            'draw': self.drawPlanes,
            'retry': self.retry,
            'start': self.startGame
        }

        self.INVALID_COMMAND = 'Invalid command, please try again.'
        self.GOODBYE_MESSAGE = 'We are sorry to see you go..'

    def drawPlanes(self):
        playerBoard = self.controller.getPlayer().getStrategyBoard()
        BoardUtils.printBoardV2(playerBoard.getBoard())

        for planeIndex in range(1, 3):
            if planeIndex == 1:
                print("Please enter the start position and direction of the tail for the first plane "
                      "(format: <start_position> <direction>).")
            else:
                print("Same for the second plane. You can also go back one step by typing 'retry'.")
            planesDrawn = False
            while not planesDrawn:
                try:
                    coordinates = input("PLANE " + str(planeIndex) + ": ").strip().split()
                    if len(coordinates) != 2:
                        raise IOError("Invalid details, insert: <start_position> <direction>")
                    start_position = coordinates[0].upper()
                    direction = coordinates[1].lower()
                    self.controller.placePlane(start_position, direction)
                    planesDrawn = True
                except Exception as exception:
                    Utils.handleException(exception)

            playerBoard = self.controller.getPlayer().getStrategyBoard()
            BoardUtils.printBoardV2(playerBoard.getBoard())

        print("Your planes have been placed. If you want to draw the planes again, type 'retry', otherwise, type "
              "'start' to start the game.")

    def retry(self):
        self.controller.resetPlayerBoard()
        self.drawPlanes()

    def startGame(self):
        if self.controller.getPlayer().getNumberOfPlanes() < 2:
            raise Exception("Game cannot be started")
        self.controller.nextTurn()
        self.controller.placeOpponentPlane()

        gameOver = False
        while not gameOver:
            playerBoard = self.controller.getPlayer().getStrategyBoard()
            targetBoard = self.controller.getPlayer().getTargetBoard()
            opponentBoard = self.controller.getNextPlayer().getStrategyBoard()
            BoardUtils.printBoardV2(playerBoard.getBoard(), targetBoard.getBoard(), opponentBoard.getBoard())

            player_planes_count = self.controller.getPlayerPlanesCount()
            opponent_planes_count = self.controller.getOpponentPlanesCount()

            print("You're standing with " + str(player_planes_count) +
                  (" plane" if player_planes_count == 1 else " planes") + " alive. " +
                  "Your opponent has " + str(opponent_planes_count) +
                  (" plane" if opponent_planes_count == 1 else " planes") + " remaining.")

            if player_planes_count == 0 and opponent_planes_count == 0:
                print("It's a tie, you downed each other!")
                gameOver = True

            if opponent_planes_count == 0:
                print("You've won!")
                gameOver = True

            if player_planes_count == 0:
                print("Opponent won!")
                gameOver = True

            if not gameOver:
                self.playerStrikeBoard()
                self.controller.computerStrikeBoard()

    def playerStrikeBoard(self):
        playerStrikes = False
        while not playerStrikes:
            try:
                strikePosition = input("Strike a position: ").strip().upper()
                self.controller.strikeBoard(strikePosition)
                self.controller.nextTurn()
                playerStrikes = True
            except Exception as exception:
                Utils.handleException(exception)

    def showMenu(self):
        """
        Prints the menu options
        """
        for value in self.MENU.values():
            print(value)

    def run(self):
        while True:
            self.showMenu()
            try:
                currentCommand, currentArguments = Utils.parseCommand(input("Command: "))

                if currentCommand == "exit":
                    print(self.GOODBYE_MESSAGE)
                    break

                try:
                    currentCommand = currentCommand.lower()
                    self.commandsDictionary[currentCommand](*currentArguments)
                except KeyError:
                    print(self.INVALID_COMMAND)

            except Exception as valueError:
                Utils.handleException(valueError)
                continue
