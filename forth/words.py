from collections import OrderedDict

from .runtime_error import Forth_Runtime_WordNotFoundError
from .std.prelude import PreludeFunctions


class ForthDict:
    def __init__(self):
        # XXX: @DESIGN @WIP Why is this so damn ugly?
        self.dict = OrderedDict(
            {
                # IO
                ".": PreludeFunctions.put(),
                "READ": PreludeFunctions.ask(),
                "PEEK": PreludeFunctions.peek(),
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
                # "IF": PreludeFunctions.implies(),     -- FIXME @WIP
                # "OR": PreludeFunctions.or_word(),     -- FIXME @WIP
                # "ELSE": PreludeFunctions.else_word(), -- FIXME @WIP
                # "THEN": PreludeFunctions.end(),       -- FIXME @WIP
                # FUNCTIONS
                ":": PreludeFunctions.colon(),
                ";": PreludeFunctions.semicolon(),
                "CREATE": PreludeFunctions.create(),  # exposing the POWER
                "WORD": PreludeFunctions.word(),
                "WORDS": PreludeFunctions.words(),
                # environment
                "$": PreludeFunctions.env(),
                "EXPORT": PreludeFunctions.setenv(),
                # Shell
                "?": PreludeFunctions.run_command(),
                # "|": PreludeFunctions.pipe(),         -- FIXME @WIP
                # "<-": PreludeFunctions.tofile(),      -- FIXME @WIP
                # State                                 -- TODO @DESIGN @WIP:
                #                                           Not really focused on state atm
                # "@": PreludeFunctions.fetchvar(),
                # "!": PreludeFunctions.definevar(),
                # Misc
                "SWAP": PreludeFunctions.swap(),
                "DUP": PreludeFunctions.dup(),
                "-.": PreludeFunctions.pop(),  #        -- FIXME: Lmao this string is literally invalid
            }
        )

    # TODO @OVERSIGHT
    # these functions are just noise, remove them soon
    def list_string(self):
        return " ".join(self.dict.keys())

    def list(self):
        return self.dict.keys()

    def new_word(self, w):
        if w in self.dict:
            print(f"Warning: redefining {w}")

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
