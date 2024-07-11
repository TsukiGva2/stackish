from .configuration import HEADER_EMPTY


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

import .std as forth_std

class WordTable:
    def __init__(self):
        self.words = {
                # IO
                   ".": forth_std.put(),
                "read": forth_std.ask(),

                # operators
                "+": forth_std.add(),
                "-": forth_std.sub(),
                "/": forth_std.div(),
                "*": forth_std.mul(),
                "^": forth_std.pow(),
                "~": forth_std.non(),

                # logic
                 "=": forth_std.equals(),
                "~=": forth_std.nequal(),
                 ">": forth_std.greater(),
                 "<": forth_std.lesser(),
                ">=": forth_std.geq(),
                "<=": forth_std.leq(),

                 "=>": forth_std.implies(),

                # environment
                "$": forth_std.env(),
                "export": forth_std.setenv(),

                # Shell
                 "?": forth_std.shell(),
                 "|": forth_std.pipe(),
                "->": forth_std.tofile(),

                # State
                "@": forth_std.fetchvar(),
                "!": forth_std.definevar(),

                # Misc
                "-.": forth_std.pop()
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
