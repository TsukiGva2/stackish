from functools import partial
from queue import deque

# - ls
# . .. .git/ main.py
# - : working_dir pwd ;
# OK WORKING_DIR
# - .. working_dir ( pwd .. )
# /home/tortea
# - echo -e "\033[32mHI"
# \033[32mHI
# - : green '(echo -e "\033[32mHI") > emit ;
# - : green '(echo -e "\033[32mHI") | '(echo) ? ;

# | -> PIPE output to next command
# > -> capture output to stack
# ? -> capture return value to stack

# TODO: the objective is a C implementation
# of this forth system

# STATES
INTERPRET = 0
COMPILE = 1

# DELIMS
DELIM_QUOTE_BEGIN = "'("
DELIM_QUOTE_END = ")"

DELIM_SQUOTE_BEGIN = "'"
DELIM_SQUOTE_END = None # applies to one word

INDEX_QUOTE_BEGIN = len(DELIM_QUOTE_BEGIN)
INDEX_QUOTE_END = -len(DELIM_QUOTE_END)

INDEX_SQUOTE_BEGIN = len(DELIM_SQUOTE_BEGIN)
#INDEX_SQUOTE_END = -len(DELIM_SQUOTE_END)

DELIM_COLON_BEGIN = ":"
DELIM_COLON_END = ";"

class Forth_UnderflowError(IndexError): ...


class Runtime:
    def __init__(self):
        self.stack = deque([])
        self.state = INTERPRET
        self.words = {}

        self.word_header = "_"

    def push(self, n):
        print(f"PUSH {n}")
    def drop(self, n):
        print(f"DROP {n}")
    def dup(self):
        print(f"DUP  {n}")

    def header(self, w):
        print(f"HEADER = {w}")

    def switch(self, s):
        print(f"STATE = {s}")

    def exec(self, code):
        for op in code:
            for f in op:
                f(self)

class Compiler:
    def __init__(self):
        self.symbols = set()
        self.words = iter([])

        self.skip = False

    # utils
    def next(self):
        try:
            return next(self.words)
        except StopIteration:
            raise EOFError("Unexpected EOF.") # TODO

    # operations
    def push(self, n):
        return (lambda state: state.push(n),)

    def drop(self, count):
        return (lambda state: state.drop(count),)

    def dup(self):
        return (lambda state: state.dup(),)

    def colon(self):
        word = self.next()
        return (lambda state: state.switch(COMPILE),
                lambda state: state.header(word))

    def endcolon(self):
        return (lambda state: state.switch(INTERPRET),)

    # makers
    def quote(self, word):
        w = word[INDEX_QUOTE_BEGIN:]

        if w.endswith(DELIM_QUOTE_END):
            return self.push(w[:INDEX_QUOTE_END])

        quote = [w]

        while not (w := self.next()).endswith(DELIM_QUOTE_END):
            quote.append(w)

        quote.append(w[:INDEX_QUOTE_END])

        result = " ".join(quote)

        return self.push(result)

    def simple_quote(self, word):
        return self.push(word[INDEX_SQUOTE_BEGIN:])

    def symbol(self, word):
        self.symbols = 0
        return self.push(0)

    def number(self, num):
        n = float(num)
        return self.push(n)

    def compile(self, words):
        self.words = iter(words)

        for w in self.words:
            meaning = ...

            if w.startswith(DELIM_QUOTE_BEGIN):
                yield self.quote(w)
                continue

            if w.startswith(DELIM_SQUOTE_BEGIN):
                yield self.simple_quote(w)
                continue

            if w == DELIM_COLON_BEGIN:
                yield self.colon()
                continue

            if w == DELIM_COLON_END:
                yield self.endcolon()
                continue

            try:
                meaning = self.number(w)
            except ValueError:
                meaning = self.symbol(w)

            yield meaning


class System:
    def __init__(self):
        self.state = Runtime()
        self.compiler = Compiler()

    def compile(self): ...
    def interpret(self): ...

    def do_string(self, line):
        if line == "":
            return "OK"

        line = line.split()

        compiled = self.compiler.compile(line)

        self.state.exec(compiled)
