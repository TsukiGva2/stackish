from .compiler import Compiler
from .runtime import Runtime


class System:
    def __init__(self):
        self.state = Runtime()

        self.compiler = Compiler()
        self.compile = self.compiler.compile

    def execute(self, instructions):
        return self.state.exec(instructions)

    def do_string(self, line):
        if line == "":
            return "OK"

        line = line.split()

        compiled = self.compiler.compile(line)
        return self.state.exec(compiled)
