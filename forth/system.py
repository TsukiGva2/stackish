from .checker import CheckedExpr
from .compiler import Compiler
from .errors import Forth_InvalidExpr
from .runtime import Runtime


class System:
    def __init__(self, shell=None):
        self.state = Runtime(shell)
        self.compiler = Compiler()

        self.checkedexpr = None

        self.InvalidExpr = Forth_InvalidExpr

    def command(self, command):
        self.checkedexpr = CheckedExpr(command, self.state)

    def execute(self):
        return self.state.exec(self.checkedexpr.compile())

    def do_string(self, line):
        if line == "":
            return "OK"

        line = line.split()

        compiled = self.compiler.compile(line)
        return self.state.exec(compiled)

    def script(self, line):
        compiled = self.compiler.compile(line)
        return self.state.exec(compiled)
