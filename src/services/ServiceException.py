class ServiceException(Exception):
    """
    Exception class for controller errors
    """
    def __init__(self, message=None):
        """
        Constructor for service exception class
        param message: A string representing the exception message
        """
        if message is None:
            message = "Game error!"
        self.__message = message

    @property
    def message(self):
        return self.__message

    def __str__(self):
        result = self.__message
        return result
