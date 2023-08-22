from collections.abc import Iterable as _Iterable
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
    return all(isinstance(arg, int) for arg in args[:2])

class FunctionalList(list):
    """
    Extends Python's list with a cleaner interface for certain practices.
    """
    def allmatch(self, callbackfn):
        """
        Returns True if every element in the list satisfies the callback function.
        """
        vals = [ch for ch in self if ch not in _STRIP_CHARS]
        res = list(filter(callbackfn, vals))
        if self and isinstance(callbackfn(vals[0]), bool):
            return len(vals) == len(res)
        return False

    def modify_range(self, *args):
        """
        Modifies a range of elements within the list by removing and inserting items.
        :param: arg 1 must be an integer specifying where to start removing
                element(s).
        :param: arg 2 must be an integer specifying the number of elements to remove.
        :param: *args => Any number of elements to be inserted.
        """
        argslen = len(args)
        if argslen == 1:
            if argtype(*args):
                self.pop(args[0])
                return
            raise TypeError("arg 1 must be an int")
        if argslen >= 2:
            startindex, delcount, *items = args
            if argtype(*args):
                if items:
                    self[startindex: startindex + delcount] = [i for i in items]
                    return
                self[startindex: startindex + delcount] = []
                return
            raise TypeError("arg 1 and 2 must be ints")

    def foreach(self, callbackfn):
        """
        Applies a function to each item in the list and returns a new processed list.
        """
        arg = type(callbackfn)
        if arg in _FUNCTIONSTYPES:
            return [callbackfn(item) for item in self]
        raise TypeError("arg 1 must be a function")
