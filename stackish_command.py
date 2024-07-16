import subprocess
from typing import final


class CommandNotFound(FileNotFoundError): ...


@final
class Command:
    def __init__(self, cmdline: str = ""):
        self.cmdline: str = cmdline
        self.args: list[str] = cmdline.split()

        self.process: subprocess.Popen = None

    def execute(self):
        return self.run_command(self.cmdline)

    def run_command(self, command, **kwargs) -> int:
        process = self.spawn(command, **kwargs)

        if not process:
            return 1

        return process.wait()

    def spawn(self, command, **kwargs) -> subprocess.Popen:
        """
        Run command
        """
        if command == "":
            raise ValueError("Can't run empty command")

        try:
            return subprocess.Popen(self.args, **kwargs)
        except FileNotFoundError:
            raise CommandNotFound("Command not found")
