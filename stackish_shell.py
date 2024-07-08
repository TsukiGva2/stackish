import sys
from typing import final, override

from stackish_command import Command, CommandNotFound
from stackish_input import ReadLine


class ConditionalREPL:
    """
    Read
    Eval
    Print
    Loop

    Conditional means it has to
    keep running under a certain
    condition
    """

    def __init__(self): ...

    def read(self): ...
    def eval(self): ...

    # def print(self): ...

    @final
    def loop(self):
        while ...:
            self.read()
            self.eval()

            # self.print()

            if not self.condition():
                return

    def condition(self): ...


@final
class Shell(ConditionalREPL):
    def __init__(self):
        self.command: Command = Command()
        self.prompt: str = "- "
        self.status: int = 0  # TODO: enum like

    @override
    def eval(self):
        try:
            self.status = self.command.execute()
        except CommandNotFound:
            sys.stderr.write("  ^^^ Command not found\n")

    @override
    def read(self):
        line = str(ReadLine(self.prompt))
        self.command = Command(line)

    @override
    def condition(self) -> bool:  # TODO
        return True
