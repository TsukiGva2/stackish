import sys
from typing import Final

from stackish_shell import Shell


def main():
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
