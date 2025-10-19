# Test file to check if type checkers find our stubs
import toolz
import tlz

# Test that type checkers recognize our stubs
x = toolz.identity(5)
y = tlz.identity(10)

reveal_type(x)  # type: ignore
reveal_type(y)  # type: ignore