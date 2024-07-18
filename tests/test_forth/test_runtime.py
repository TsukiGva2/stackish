from forth.system import System


def test_runtime_literals():
    system = System()

    stack, reports = system.do_string("'foo '(bar) 1 1e6")

    assert list(stack) == ["foo", "bar", 1, 1e6]
