from collections import OrderedDict

from .configuration import HEADER_EMPTY
from .errors import Forth_HeaderRedefinitionError, Forth_NotFound
from .std.prelude import PreludeFunctions


class DictEntry:
    def __init__(self, header=HEADER_EMPTY):
        self.header = header
        self.data = []

    def set_word(self, w):
        if self.header != HEADER_EMPTY:
            raise Forth_HeaderRedefinitionError(
                f"Trying to change unclosed WordHeader name: '{self.header}' -> {w}"
            )

        self.header = w

    def pack(self):
        return {self.header: self.data}

    def new(self, w=HEADER_EMPTY):
        self.header = w
        self.data = []

    def insert(self, instruction):
        self.instructions.append(instruction)


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
                #                                       -- NOTE @DESIGN: That's kind of ugly
                "swap": PreludeFunctions.swap(),
                "dup": PreludeFunctions.dup(),
                "-.": PreludeFunctions.pop(),  #        -- FIXME: Lmao this string is literally invalid
            }
        )

        # self.word

    def list_string(self):
        return " ".join(self.words.keys())

    def list(self):
        return self.words.keys()

    def new_word(self, w=HEADER_EMPTY):
        self.word_head
        self.word_defs.append(DictEntry(w))
        return w

    def set_header_word(self, w):
        self.header.set_word(w)
        return w

    def insert(self, instruction):
        self.header.insert(instruction)

        return instruction.name

    def find(self, w):
        try:
            return self.words[w]
        except KeyError:
            raise Forth_NotFound(f"Undefined word {w}")
