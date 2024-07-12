from .compiler import Compiler
from .runtime import Runtime


class Forth_NotFound(Exception): ...


class System:
    def __init__(self, shell=None):
        self.state = Runtime(shell)
        self.compiler = Compiler()

        self.NotFound = Forth_NotFound

    def do_string(self, line):
        if line == "":
            return "OK"

        line = line.split()

        compiled = self.compiler.compile(line)
        return self.state.exec(compiled)

    def script(self, line):
        compiled = self.compiler.compile(line)
        return self.state.exec(compiled)
