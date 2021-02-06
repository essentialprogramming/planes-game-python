import string


class NumberUtils:

    @staticmethod
    def ordinal(letter):
        if len(letter) != 1:
            return 0
        position = ord(letter)
        if 65 <= position <= 90:
            # Upper case letter
            return position - 65
        elif 97 <= position <= 122:
            # Lower case letter
            return position - 97
        # Unrecognized character
        return 0

    @staticmethod
    def letter(index):
        return chr(ord('A') + index)

    @staticmethod
    def alphabet_position(text):
        nums = [str(ord(x) - 96) for x in text.lower() if 'a' <= x <= 'z']
        return " ".join(nums)
