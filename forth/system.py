from .compiler import Compiler
from .errors import Forth_InvalidExpr
from .runtime import Runtime


class System:
    def __init__(self):
        self.state = Runtime()

        self.compiler = Compiler()
        self.compile = self.compiler.compile

        self.InvalidExpr = Forth_InvalidExpr

    def execute(self, instructions):
        return self.state.exec(instructions)

    def do_string(self, line):
        if line == "":
            return "OK"

        line = line.split()

        compiled = self.compiler.compile(line)
        return self.state.exec(compiled)

    def script(self, line):
        compiled = self.compiler.compile(line)
        return self.state.exec(compiled)
