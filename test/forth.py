import forth.system as sf
from stackish_shell import Shell


def dostring(code):
    shell = Shell()
    s = sf.System(shell=shell)

    print(s.do_string(code))
    print(s.state.stack)


def functions():
    dostring(
        """
        : numbers
            1 2 3 4
        ;

        : duplicate
            numbers numbers
        ;

        duplicate
    """
    )

    dostring(
        """
            : google
                '(ping -c 1 www.google.com) ?
                0 ~= =>
                    '(error)
                or
                    '(success)
                end
                .
            ;
            google
        """
    )


def run():
    functions()
