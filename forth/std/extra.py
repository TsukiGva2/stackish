# Extra functionality for the forth system

from forth.instruction import Instruction


class ExtraFunctions:
    # saving and loading files
    @staticmethod
    def save():
        return Instruction(lambda _: _, name="save")

    @staticmethod
    def load():
        return Instruction(lambda _: _, name="save")
