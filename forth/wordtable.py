from .configuration import HEADER_EMPTY
from .std import StdFunctions


class WordHeader:
    def __init__(self, header=HEADER_EMPTY):
        self.header = header
        self.instructions = []

    def pack(self):
        return {self.header: self.instructions}

    def clear(self):
        self.header = HEADER_EMPTY
        self.instructions = []

    def insert(self, instruction):
        self.instructions.append(instruction)


class WordTable:
    def __init__(self):
        self.words = {
            # IO
            ".": StdFunctions.put(),  # : . '(echo) ? ;
            "read": StdFunctions.ask(),
            # operators
            "+": StdFunctions.add(),
            "-": StdFunctions.sub(),
            "/": StdFunctions.div(),
            "*": StdFunctions.mul(),
            "^": StdFunctions.pow(),
            "~": StdFunctions.non(),
            # logic
            "=": StdFunctions.equals(),
            "~=": StdFunctions.nequals(),
            ">": StdFunctions.greater(),
            "<": StdFunctions.lesser(),
            ">=": StdFunctions.greater_or_equals(),
            "<=": StdFunctions.lesser_or_equals(),
            "=>": StdFunctions.implies(),
            "or": StdFunctions.or_word(),
            # "else": StdFunctions.else_word(), -- FIXME @WIP
            "end": StdFunctions.end(),
            # environment
            "$": StdFunctions.env(),
            "export": StdFunctions.setenv(),
            # Shell
            "?": StdFunctions.run_command(),
            # "|": StdFunctions.pipe(), -- FIXME @WIP
            # "<-": StdFunctions.tofile(), -- FIXME @WIP
            # State -- TODO @DESIGN @WIP: Not really focused on state atm
            # "@": StdFunctions.fetchvar(),
            # "!": StdFunctions.definevar(),
            # Misc
            # NOTE @DESIGN: That's kind of ugly
            "-.": StdFunctions.pop(),
        }

        self.header = WordHeader()

    def new(self, w):
        self.header = WordHeader(w)
        return w

    def end(self):
        name = self.header.header

        self.words.update(self.header.pack())
        self.header.clear()

        return name

    def insert(self, instruction):
        self.header.insert(instruction)

        return instruction.name

    def find(self, w):
        return self.words[w]
