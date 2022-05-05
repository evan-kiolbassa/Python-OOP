'''
__mro__ returns the method resolution orders to see their inheritance graphs
'''
IndexError.__mro__
KeyError.__mro__

'''
The parent node for each error above is LookupError,
thus both errors can be robustly handled using LookUpError
'''

def lookups():
    s = [1, 4, 6]
    try:
        item = s[5]
    except LookupError:
        print("Handled IndexError")
    
    d = dict(a = 65, b = 66, c = 67)
    try:
        value = d['x']
    except LookupError:
        print('Handled Key Error')

'''
BaseException is a base class of all exception types
'''

'''
The function defined below robustly handles the case of an empty series

'''
def median(iterable):
    items = sorted(iterable)
    if len(items) == 0:
        raise ValueError("Median() arg is an empty series")
    median_index = (len(items) - 1) // 2
    if len(items) % 2 != 0:
        return items[median_index]
    return (items[median_index] + items[median_index] + 1) / 2


'''
The three Print() commands output the following error statements;
Payload ('Median() arg is an empty series',)
Payload repr: ValueError('Median() arg is an empty series')
Payload str: Median() arg is an empty series
'''
def main():
    try:
        median([])
    except ValueError as e:
        print('Payload', e.args)
        print("Payload repr:", repr(e))
        print('Payload str:', str(e))

main()

'''
Best-practices dictate that an Error-Constructor should contain only
a single string entry in args. The string is stored within a tuple.

However, the unicode example shown below illustrates a case where the 
error has various attributes that add depth to the error message.

Therefore, additional string inputs should be stored in other Constructor attributes
'''

def main():
    try:
        b'\x81'.decode('utf-8')
    except UnicodeError as e:
        print(e)
        print('encoding:', e.encoding)
        print("reason:", e.reason)
        print("object:", e.object)
        print('Start:', e.start)
        print("end:", e.end)

import math
from re import X
from tarfile import BLOCKSIZE
from typing_extensions import Self
from unittest import result

class TriangleError(Exception):
    '''
    __init__ message that accepts a message and collection of side lengths.
    The message is forwarded to the base Class Exception constructor for stoarage
    Side attributes are stored on an instance attribute of the derived class.
    The tuple structure is used to prevent modification and provide a read-only
    method for accessing the side data
    '''
    def __init__(self, text, sides):
        super().__init__(text)
        self._sides = tuple(sides)

    @property
    def sides(self):
        return self._sides

    def __str__(self):
        return "'{}' for sides {}".format(self.args[0], self._sides)

    def __repr__(self):
        return "TriangleError({!r})".format(self.args[0], self._sides)

def triangle_area(a, b, c):
    sides = sorted((a, b, c))
    if sides[2] > sides[0]+ sides[1]:
        raise TriangleError("Illegal Triangle", sides)
    p = (a + b + c) / 2
    a = math.sqrt(p * (p-a) * (p-b) * (p-c))
    return a

# Explicit Exception Chaining / Implicit
# Implicit chaining
import io
def main():
    try:
        a = triangle_area(3, 4, 10)
        print(a)
    except TriangleError as e:
        try:
            print(e, file = sys.stdin)
        except io.UnsupportedOperation as f:
            print(e)
            print(f)
            print(f.__context__ is e)

class InclinationError(Exception):
    pass

def inclination(dx, dy):
    try:
        return math.degrees(math.atan(dy / dx))
    except ZeroDivisionError as e:
        raise InclinationError("Slope Cannot be Vertical") from e

'''
__traceback__ : Attribute on an exception object that holds a 
reference to the traceback object
'''

from traceback import print_tb

class InclinationError(Exception):
    pass

def inclination(dx, dy):
    try:
        return math.degrees(math.atan(dy / dx))
    except ZeroDivisionError as e:
        raise InclinationError("Slope Cannot be Vertical") from e

def main():
    try:
        inclination(0, 5)
    except InclinationError as e:
        print(e.__traceback__)
        print_tb(e.__traceback)
        print("Finished")

'''
Summary of Python Tracebacks;
Tracebacks in Python are objects

They are stored on __traceback__ attribute on exceptions class

The traceback module provides functions
to work with tracebacks

Avoid storing tracebacks for too long due to the memory allocation
requirements of traceback storage
'''



'''
Assertions as a method of error-handling.

Assertions monitor invariants that should always be True in your code base.

A failing assertion points to a programming error
'''
# assert condition [, message]
assert False, "The condition was False"


'''
If the assertion that you make is False, no exception is raised and the script continues
'''
assert 5 > 2, "You are living in a defective universe!"

'''
Assertions are best used to document conditions your program takes for granted
'''

def modulus_four():
    r = n % 4
    if r == 0:
        print("Multiple of 4")
    elif r == 1:
        print("Remainder 1")
    elif r == 2:
        print("Remainder 2")
    elif r == 3:
        print("Remainder 3")
    else:
        assert False, "This is not Possible!"

'''
Assertion statements should only be used to validate implemenations
or errors made by the programmer.

Assertions shoul not be used to vailifate functon arguments due to the computational cost
'''

from bisect import bisect_left

class sorted_set:
    def __init__(self,xs):
        self._set = []
        for x in xs:
            self.add(x)

    def add(self, x):
        self._set.append(x)
        self._set = sorted(set(self._set))
        assert self._is_unique_and_sorted()

    def contains(self, x):
        assert self._is_unique_and_sorted()
        index = bisect_left(self._set, x)
        return index != len(self._set) and self._set[index] == X

    def _is_unique_and_sorted(self):
        return all(self._set[i] < self._set[i + 1] for i in range(len(self._set) - 1))


def wrap(text, line_length):
    '''
    A function that splits string objects into lines that are less-than 
    or equal to the line_length arg.

    Uses an assert statement to check if all linesmeet the line length
    requirement.
    '''
    if line_length < 1:
        raise ValueError("Line length {} is not positive".format(line_length))

    words = text.split()

    if (max(map(len, words))) > line_length:
        raise ValueError("Line length must be at least as long as the longest word")

    lines_of_words = []
    current_line_length = line_length
    for word in words:
        if current_line_length + len(word) > line_length:
            lines_of_words.append([]) # Creation of a new line
        lines_of_words[-1].append(word)
        current_line_length += len(word) + len(' ')
    lines = [' '.join(line_of_words) for line_of_words in lines_of_words]
    result = '\n'.join(lines)

    assert all(len(line) <= line_length for line in result.splitlines())

    return result

'''
Context Managers

A context manager is an object designed to be used in a with statement.

Ensures that resources are properly and automatically handled.
The "enter" method ensures that the resource is ready for use.

The "exit" method ensures that the resource is cleaned up.
'''


class LoggingContextManager:
    def __enter__(self):
        print('LoggingContextManager.__enter__()')
        return "You're in a with-block!"

    '''
    The __exit__() method is executed after with-block terminates and
    handles exceptional exits from the with-block.

    Reveives the exception type, value, and traceback.

    The arguments are None when exceptions are not raised.
    Output for normal termination is different from output with termination with exception.
    '''
    def __exit__(self, exc_type,exc_val, exc_tb):
        if exc_type is None:
            print('LoggingContextManager.__exit__: '
                  'normal exit detected')

        else:
            print('LoggingContextManager.__exit__:'
            'Exception Detected!'
            'type={}, value={}, traceback= {}'.format(exc_type,exc_val, exc_tb))


mgr = (EXPR)
exit = type(mgr).__exit__() # Not calling it yet
value = type(mgr).__enter__(mgr)
exc = True
try:
    try:
        VAR = value #Only if "as VAR is present"
        BLOCK
    except:
        # The exceptional case is handled here
        exc = False
        if not exit(mgr, *sys.exc_info()):
            raise
        # the exception is swallowed if exit() returns True
finally:
    # The normal and non-local-goto cases are handled here
    if exc:
        exit(mgr, None, None, None)


import contextlib
import sys

@contextlib.contextmanager
def logging_context_manager():
    print('logging_context_manger: enter')
    try:
        yield "You're in a with-block!"
        print('logging_context_manager: normal exit')
    except Exception:
        print('logging_context_manager: exceptional exit',
            sys.exc_info)
              