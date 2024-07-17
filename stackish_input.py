import readline
from typing import final

readline.parse_and_bind("tab: complete")
readline.set_completer_delims(" \t\n`~!@#$%^&*()-=+[{]}\\|;:'\",<>/?")


@final
class ReadLine:
    def __init__(self, prompt="> ", words=[], non_empty=True):
        while (line := input(prompt)) == "" and non_empty:
            ...
        self.line = line

    def __str__(self):
        return self.line
