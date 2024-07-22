import sys
from typing import Final

from forth.system import System
from repl.shell import Shell


def main():
    forth: Final[System] = System()
    shell: Final[Shell] = Shell(forth)

    while True:
        try:
            shell.loop()
        except EOFError:
            print("\nEOF")
            return True
        except Exception as err:
            print(f"\n| Exception: {err}")

    # unreachable
    # return True


if __name__ == "__main__":
    if not main():
        sys.exit(1)
