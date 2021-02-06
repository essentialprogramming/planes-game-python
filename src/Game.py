from domain.Player import Player

from services.GameService import GameService

from ui.UI import UI

player = Player()
computer = Player()

try:
    settingsFile = open("settings.properties", "r")

    difficultyInput = settingsFile.readline().strip()
    if len(difficultyInput) == 0:
        raise IOError("Difficulty option not given, check settings.properties file.")
    difficulty = difficultyInput.split("=")[1]

    if difficulty != "medium" and difficulty != "hard":
        raise IOError("The difficulty option in settings.properties must be either 'medium' or 'hard'.")

    gameService = GameService(player, computer, difficulty)
    console = UI(gameService)
    console.run()

    settingsFile.close()
except IOError as io_error:
    raise io_error
