import re
from collections import deque

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
DELIM_SQUOTE_END = None  # applies to one word

INDEX_QUOTE_BEGIN = len(DELIM_QUOTE_BEGIN)
INDEX_QUOTE_END = -len(DELIM_QUOTE_END)

INDEX_SQUOTE_BEGIN = len(DELIM_SQUOTE_BEGIN)
# INDEX_SQUOTE_END = -len(DELIM_SQUOTE_END)

DELIM_COLON_BEGIN = ":"
DELIM_COLON_END = ";"

HEADER_EMPTY = "_"



class Forth_UnderflowError(IndexError): ...
class Forth_EvaluationError(RuntimeError): ...
class Forth_CompilationError(SyntaxError): ...



class WordHeader:
    def __init__(self, header=HEADER_EMPTY):
        self.header = header
        self.instructions = []

    def compile(self):
        return {self.header: self.instructions}

    def clear(self):
        self.header = HEADER_EMPTY
        self.instructions = []

    def insert(self, instruction):
        self.instructions.append(instruction)



class WordTable:
    def __init__(self):
        self.words = {}

        self.header = WordHeader()

    def new(self, w):
        self.header = WordHeader(w)
        return w

    def end(self):
        name = self.header.header

        self.words.update(self.header.compile())
        self.header.clear()

        return name

    def insert(self, instruction):
        self.header.insert(instruction)

        return instruction.name

    def find(self, w):
        return self.words[w]



class Runtime:
    def __init__(self):
        self.stack = deque([])
        self.state = INTERPRET
        self.words = WordTable()

    # operations
    def push(self, *args):
        self.stack.extend(args)

        return args

    def drop(self):
        self.stack.pop()

        return 0

    def dup(self):
        n = self.stack.pop()
        self.push(n, n)

        return n

    def header(self, w):
        return self.words.new(w)

    def close_header(self):
        return self.words.end()

    def fetch(self, w):
        instructions = self.words.find(w)
        self.exec(instructions)

        return w

    def insert(self, w):
        return self.words.insert(w)

    def switch(self, s):
        if self.state == s:
            raise Forth_EvaluationError("Unexpected state switch (double :/;)")

        self.state = s

        return s

    # functs
    def eval(self, instruction):
        return instruction.run(self)

    def exec(self, instructions):
        return [self.eval(i) for i in instructions]



class Instruction:
    def __init__(self, *operations, name = "_", compiled = True):
        self.operations = operations

        self.name = name
        self.compiled = compiled

        # print(f"generated: {name}")

    def run(self, state):
        if not self.compiled or state.state == INTERPRET:
            return [op(state) for op in self.operations]

        return state.insert(self)



class Compiler:
    def __init__(self):
        self.symbols = set()
        self.words = iter([])

        self.skip = False

        self.match_word = re.compile(
            r"[?/A-Za-z!@#$%&*()\[\]^~'`\"\\+=-_.,><{}][?/A-Za-z0-9!@#$%&*()\[\]^~'`\"\\+=-_.,><{}]+"
        )

    # utils
    def next(self):
        try:
            return next(self.words)
        except StopIteration:
            raise EOFError("Unexpected EOF.")  # TODO

    def word(self, w):
        if self.match_word.match(w):
            return w
        raise Forth_CompilationError(f"Invalid identifier '{w}")

    # operations
    def push(self, n):
        return Instruction(
            lambda state: state.push(n),
            name = f"PUSH {n}"
        )

    def drop(self, count):
        return Instruction(
            lambda state: state.drop(count),
            name = f"DROP {count}"
        )

    def dup(self):
        return Instruction(
            lambda state: state.dup(),
            name = "DUP"
        )

    def colon(self):
        word = self.word(self.next())
        return Instruction(
            lambda state: state.switch(COMPILE),
            lambda state: state.header(word),
            name = f"FUNC {word}",
            compiled = False
        )

    def endcolon(self):
        return Instruction(
            lambda state: state.switch(INTERPRET),
            lambda state: state.close_header(),
            name = "END",
            compiled = False
        )

    def find(self, word):
        return Instruction(
            lambda state: state.fetch(word),
            name = f"FIND {word}"
        )

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
        w = self.word(word)

        return self.find(w)

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

    def do_string(self, line):
        if line == "":
            return "OK"

        line = line.split()

        compiled = self.compiler.compile(line)

        return self.state.exec(compiled)
