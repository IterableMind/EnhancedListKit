import types
import string

_FUNCTIONSTYPES = [
    types.FunctionType,
    types.MethodDescriptorType,
    types.MethodType,
    types.BuiltinFunctionType
]

_STRIP_CHARS = list(string.whitespace + string.punctuation)

def argtype(*args):
    """
    Check if the first two arguments are integers.
    """
    return all(isinstance(arg, int) for arg in args[:2])

class FunctionalList(list):
    """
    Extends Python's list with a cleaner interface for certain practices.
    """

    def all_match(self, callback):
        """
        Returns True if every element in the list satisfies the callback
        function else False.
        """
        elements = [c for c in self if c not in _STRIP_CHARS]
        if self and isinstance(callback(elements[0]), bool):
            return len(elements) == len([v for v in filter(callback, elements)])
        return False  # Empty list

    def splice(self, startindex, delcount, *items):
        """
        Modifies a range of elements within the list by removing and inserting items.
        """
        if not argtype(startindex, delcount):
            raise TypeError('startindex and delcount must be integers')

        if startindex >= len(self):
            raise IndexError('startindex is out of range')

        if len(self) < delcount:
            raise IndexError(f'Trying to remove {delcount} elements but only {len(self)} present')

        if items:
            self[startindex: startindex + delcount] = list(items)
        else:
            self[startindex: startindex + delcount] = []

    def for_every(self, callback):
        """
        Applies a function to each item in the list and returns a new processed list.
        """
        if isinstance(callback, tuple(_FUNCTIONSTYPES)):
            return [callback(item) for item in self]
        raise TypeError('arg 1 must be a function')

