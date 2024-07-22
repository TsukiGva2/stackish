from collections import OrderedDict

from .log import Forth_Log
from .runtime_error import Forth_Runtime_WordNotFoundError
from .std.prelude import Prelude, PreludeFunctions


class ForthDict:
    def __init__(self):
        # XXX: @DESIGN @WIP Why is this so damn ugly?
        self.dict: OrderedDict = Prelude.copy()

    # TODO @OVERSIGHT
    # these functions are just noise, remove them soon
    def list_string(self):
        return " ".join(self.dict.keys())

    def list(self):
        return self.dict.keys()

    def reset(self):
        self.dict = Prelude.copy()

    def new_word(self, w):
        if w in self.dict:
            Forth_Log(f"Warning: redefining {w}")

        self.dict |= {w: PreludeFunctions.nop()}

        self.dict.move_to_end(w)

    def insert(self, instruction):
        tail = next(reversed(self.dict))

        self.dict[tail] += instruction
        return instruction.name

    def find(self, w):
        try:
            return self.dict[w]
        except KeyError:
            raise Forth_Runtime_WordNotFoundError(f"Undefined word {w}")
