from .configuration import HEADER_EMPTY
from .errors import Forth_HeaderRedefinitionError, Forth_NotFound
from .std import StdFunctions


class WordHeader:
    def __init__(self, header=HEADER_EMPTY):
        self.header = header
        self.instructions = []

    def set_word(self, w):
        if self.header != HEADER_EMPTY:
            raise Forth_HeaderRedefinitionError(
                f"Trying to change unclosed WordHeader name: '{self.header}' -> {w}"
            )

        self.header = w

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
            ":": StdFunctions.colon(),
            ";": StdFunctions.endcolon(),
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
            "swap": StdFunctions.swap(),
            "-.": StdFunctions.pop(),
        }

        self.header = WordHeader()

    def new(self, w=HEADER_EMPTY):
        self.header = WordHeader(w)
        return w

    def set_header_word(self, w):
        self.header.set_word(w)
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
        try:
            return self.words[w]
        except KeyError:
            raise Forth_NotFound(f"Undefined word {w}")
