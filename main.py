from typing import final, override, Final
import subprocess
import readline
import sys


@final
class ReadLine:
    def __init__(self, prompt="> ", words=[], non_empty=True):
        while (line := input(prompt)) == "" and non_empty: ...
        self.line = line

    def __str__(self):
        return self.line


class CommandNotFound(FileNotFoundError): ...


@final
class Command:
    def __init__(self, cmdline: str = ""):
        self.cmdline: str = cmdline
        self.args: list[str] = cmdline.split()

        self.process: subprocess.Popen = None

    def execute(self) -> int:
        """
        Run command and return the status code
        """
        if self.cmdline == "":
            raise ValueError("Can't run empty command")

        try:
            self.process = (
                subprocess.Popen(
                    self.args,
                    #stderr = subprocess.PIPE
                )
            )
        except FileNotFoundError:
            raise CommandNotFound("Command not found")

        return self.process.wait()


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
    def condition(self) -> bool:
        return self.status == 0


def main():
    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims(" \t\n`~!@#$%^&*()-=+[{]}\\|;:\'\",<>/?")

    shell: Final[Shell] = Shell()

    try:
        shell.loop()
    except EOFError:
        print("\nEOF")
        return True
    except Exception as err:
        print(f"\n| Exception: '{err}'")
        return False

    return True


if __name__ == "__main__":
    if not main():
        sys.exit(1)
