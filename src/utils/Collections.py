from copy import deepcopy


class Collections:

    # Yield successive n-sized
    # chunks from l.
    @staticmethod
    def divideChunks(aList, n):
        for i in range(0, len(aList), n):
            yield aList[i:i + n]

    @staticmethod
    def split(aList, n):
        return list(Collections.divideChunks(aList, n))
