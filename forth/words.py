from collections import OrderedDict

from .configuration import HEADER_EMPTY
from .errors import Forth_NotFound
from .instruction import Instruction
from .std.prelude import PreludeFunctions


class DictEntry:
    def __init__(self, header=HEADER_EMPTY):
        self.header = header
        self.flags = {"compiled": True}
        self.code = []

    def pack(self):
        return {self.header: Instruction(*self.data, **self.flags)}

    def new(self, w=HEADER_EMPTY):
        self.header = w
        self.code = []

    def set_flags(self, **kwargs):
        self.flags = kwargs

        return kwargs

    def insert(self, instruction):
        self.code.append(instruction)


class Words:
    def __init__(self):
        # XXX: @DESIGN @WIP Why is this so damn ugly?
        self.words = OrderedDict(
            {
                # IO
                ".": PreludeFunctions.put(),
                "read": PreludeFunctions.ask(),
                # operators
                "+": PreludeFunctions.add(),
                "-": PreludeFunctions.sub(),
                "/": PreludeFunctions.div(),
                "*": PreludeFunctions.mul(),
                "^": PreludeFunctions.pow(),
                "~": PreludeFunctions.non(),
                # logic
                "=": PreludeFunctions.equals(),
                "~=": PreludeFunctions.nequals(),
                ">": PreludeFunctions.greater(),
                "<": PreludeFunctions.lesser(),
                ">=": PreludeFunctions.greater_or_equals(),
                "<=": PreludeFunctions.lesser_or_equals(),
                # IF THEN
                # "if": PreludeFunctions.implies(),     -- FIXME @WIP
                # "or": PreludeFunctions.or_word(),     -- FIXME @WIP
                # "else": PreludeFunctions.else_word(), -- FIXME @WIP
                # "then": PreludeFunctions.end(),       -- FIXME @WIP
                # FUNCTIONS
                # ":": PreludeFunctions.colon(),        -- FIXME @WIP
                # ";": PreludeFunctions.endcolon(),     -- FIXME @WIP
                "WORD": PreludeFunctions.word(),
                "words": PreludeFunctions.words(),
                # environment
                "$": PreludeFunctions.env(),
                "export": PreludeFunctions.setenv(),
                # Shell
                "?": PreludeFunctions.run_command(),
                # "|": PreludeFunctions.pipe(),         -- FIXME @WIP
                # "<-": PreludeFunctions.tofile(),      -- FIXME @WIP
                # State                                 -- TODO @DESIGN @WIP:
                #                                           Not really focused on state atm
                # "@": PreludeFunctions.fetchvar(),
                # "!": PreludeFunctions.definevar(),
                # Misc
                "swap": PreludeFunctions.swap(),
                "dup": PreludeFunctions.dup(),
                "-.": PreludeFunctions.pop(),  #        -- FIXME: Lmao this string is literally invalid
            }
        )

        self.header = DictEntry()

    def list_string(self):
        return " ".join(self.words.keys())

    def list(self):
        return self.words.keys()

    def new_word(self, w=HEADER_EMPTY):
        self.header.new(w)
        return w

    def insert(self, instruction):
        self.header.insert(instruction)
        return instruction.name

    def find(self, w):
        try:
            return self.words[w]
        except KeyError:
            raise Forth_NotFound(f"Undefined word {w}")
