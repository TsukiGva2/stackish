from collections import OrderedDict

from .errors import Forth_NotFound
from .std.prelude import PreludeFunctions


class ForthDict:
    def __init__(self):
        # XXX: @DESIGN @WIP Why is this so damn ugly?
        self.dict = OrderedDict(
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

    # TODO @OVERSIGHT
    # these functions are just noise, remove them soon
    def list_string(self):
        return " ".join(self.words.keys())

    def list(self):
        return self.words.keys()

    def new_word(self, w):
        if w in self.dict:
            print(f"Warning: redefining {w}")

        self.dict |= {w: PreludeFunctions.nop()}

    def insert(self, instruction):
        tail = next(reversed(self.dict))

        self.dict[tail] += instruction
        return instruction.name

    def find(self, w):
        try:
            return self.words[w]
        except KeyError:
            raise Forth_NotFound(f"Undefined word {w}")
