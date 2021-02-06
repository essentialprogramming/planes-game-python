import _operator
import re


class Utils:
    operators = {
        "=": _operator.eq,
        "<": _operator.lt,
        ">": _operator.gt
    }

    operatorList = ["<", "=", ">"]

    @staticmethod
    def isInteger(inputData):
        return inputData.isdigit()

    @staticmethod
    def readInteger(text, condition=lambda x: True):
        while True:
            try:
                inputData = input(text)
                assert Utils.isInteger(inputData) is True
                assert condition(inputData) is True
                return int(inputData)
            except AssertionError:
                print("Invalid input, please try again.")
                pass

    @staticmethod
    def readString(text, condition=lambda x: True):
        while True:
            try:
                inputData = input(text)
                assert condition(inputData) is True
                return inputData.lstrip()
            except AssertionError:
                print("Invalid input, please try again.")
                pass

    @staticmethod
    def parseCommand(inputCommand):
        """
        Separate the command and arguments
        :param inputCommand: string
        """
        inputCommand = inputCommand.lstrip(" ")
        position = inputCommand.find(" ")

        if position == -1:
            return inputCommand, []

        command = inputCommand[: position]
        # arguments = inputCommand[position + 1:].split()
        arguments = Utils.split(inputCommand[position + 1:])

        return command, arguments

    @staticmethod
    def parseInput(inputCommand):
        """
       Separate the command and arguments
       :param inputCommand: string
        """
        inputCommand = inputCommand.lstrip(" ")
        arguments = inputCommand[0:].split()
        return arguments

    @staticmethod
    def handleException(error):
        errorString = str(error) + ", please try again"
        print(errorString)

    @staticmethod
    def split(inputString):
        def strip_quotes(s):
            if s and (s[0] == '"' or s[0] == "'") and s[0] == s[-1]:
                return s[1:-1]
            return s

        return [strip_quotes(p).replace('\\"', '"').replace("\\'", "'") \
                for p in re.findall(r'"(?:\\.|[^"])*"|\'(?:\\.|[^\'])*\'|[^\s]+', inputString)]
