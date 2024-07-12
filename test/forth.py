import forth.system as sf
from stackish_shell import Shell


def dostring(code):
    shell = Shell()
    s = sf.System(shell=shell)

    s.do_string(code)
    #print(s.state.stack)


def functions():
    print("testing functions: ")

    print("nesting: ")
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
                '(hey) . 12 3 45
            ;

            : wow 1 1 = => 'cool . end ;
            0 0 = => wow end 1 .
        """
    )


def run():
    functions()
