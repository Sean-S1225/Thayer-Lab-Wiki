from typing import Callable

class WrongExceptionException(Exception):
    pass

def JoinTupleStr(join: str) -> Callable[[tuple], str]:
    """Given a string, returns a function that when given a tuple, will return a string containing each element in the tuple,
    with each pair of two elements separated by the string.

    Args:
        join: The string to be used to join two elements of the tuple together
    """

    def JoinTuple(t: tuple) -> str:
        return join.join([str(x) for x in t])

    return JoinTuple

def UnitTest(func: Callable, args: tuple, returns: tuple, equality: Callable = lambda x, y: x == y) -> None:
    """A simple unit tester that checks if the output of a function is what it should be

    Args:
        func: The function being tested
        args: The arguments being passed into the function
        returns: What the output should be
    """

    assert type(args) == tuple, "The type of the variable 'args' must be a tuple."
    assert type(returns) == tuple, "The type of the variable 'returns' must be a tuple."

    sep = "\n\t\t"
    joinTuple = JoinTupleStr(sep)
    assert equality((actual := (func(*args), )), returns), \
        f"\n\tFunction '{func.__name__}' failed on inputs:\n\t\t{joinTuple(args)}\n\tShould have returned:\n\t\t{joinTuple(returns)}\n\tInstead returned:\n\t\t{joinTuple(actual)}"
    
def UnitTestError(func: Callable, args: tuple, exception: Exception) -> None:
    """A unit test function designed for unit tests that will result in error; ensures the error is the correct one

    Args:
        func: The function being tested
        args: The arguments being passed into the function
        exception: The exception expected
    """

    try:
        func(*args)
    except exception:
        pass
    except Exception as e:
        raise WrongExceptionException(f"Expected exception of type {exception}, instead got error of type {type(e)}")