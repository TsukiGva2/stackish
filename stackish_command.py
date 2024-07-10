import subprocess
from typing import final


class CommandNotFound(FileNotFoundError): ...


@final
class Command:
    def __init__(self, cmdline: str = "", commander=None):
        self.cmdline: str = cmdline
        self.args: list[str] = cmdline.split()

        self.commander = commander

        self.process: subprocess.Popen = None

    def execute(self) -> int:
        """
        Run command and return the status code
        """
        if self.cmdline == "":
            raise ValueError("Can't run empty command")

        try:
            self.process = subprocess.Popen(
                self.args,
                # stderr = subprocess.PIPE
            )
        except FileNotFoundError:
            raise CommandNotFound("Command not found")

        return self.process.wait()
