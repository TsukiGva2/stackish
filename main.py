from typing import final, override, Final
import subprocess
import sys

@final
class ReadLine:
    def __init__(self, prompt="> ", non_empty=True):
        while (self.line := input(prompt)) == "" and non_empty: ...

    def __str__(self):
        return self.line

@final
class Command:
    def __init__(self, cmdline: str = ""):
        self.cmdline: str = cmdline
        self.args: list[str] = cmdline.split()

    def execute(self) -> int:
        """
        Run command and return 
        """
        if self.cmdline == "":
            raise ValueError("Can't run empty command")

        subprocess.Popen()

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
    def print(self): ...

    @final
    def loop(self):
        while ...:
            self.read()
            self.eval()
            self.print()

            if not self.condition():
                return

    def condition(self): ...

@final
class Shell(ConditionalREPL):
    def __init__(self):
        self.command: Command = Command(None)
        self.prompt: str = "- "
        self.status: int = 0 # TODO: enum like

    @override
    def eval(self):
        self.status = self.command.execute()

    @override
    def read(self):
        line = str(ReadLine(self.prompt))
        self.command = Command(line)

    @override
    def condition(self) -> bool:
        return self.status > 0

def main():
    shell: Final[Shell] = Shell()

    try:
        shell.loop()
    except ShellException as err:
        print(f"EXCEPTION:\n\t| '{err}'")
        return False

    return True

if __name__ == "__main__":
    if not main():
        sys.exit(1)

