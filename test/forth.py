import forth.system as sf


def dostring(code):
    s = sf.System()
    print(s.do_string(code))
    print(s.state.stack)


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

    print("Operations")
    dostring(
        """
            : ping '(ping www.google.com) ? => . ;
        """
    )


def run():
    functions()
