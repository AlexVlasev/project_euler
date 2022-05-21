import heapq as hq

from .errors import InvalidArgumentError


def get_triples(triple):
    """
    Get Pythagorean triples starting from a Pythagorean triple.
    This uses the Pythagorean tree matrices approach. It assumes
    the triple is given in reverse. It outputs reversed triples.
    """
    c, b, a = triple
    a2, b2, c2 = 2 * a, 2 * b, 2 * c
    c3 = 3 * c
    t1 = (-a2 + b2 + c3, -a2 + b + c2, -a + b2 + c2)
    t2 = (a2 - b2 + c3, a2 - b + c2, a - b2 + c2)
    t3 = (a2 + b2 + c3, a2 + b + c2, a + b2 + c2)
    return t1, t2, t3


class PPTIterator:
    """
    This is a Primitive Pythagorean Triple (PPT) iterator implemented using heaps.
    It starts from the smallest PPT (3, 4, 5) and generates triples up to "limit" in c-value.
    Triples are generated in increasing c-value.

    There is an optional condition function that makes the iterator only yield triples
    that satisfy the condition. This is useful for problems where triples are required
    to have a certain form.
    """
    def __init__(self, limit, condition_function=None):
        self.limit = limit
        self.heap = [(5, 4, 3)]

        if limit < 5:
            raise InvalidArgumentError(f'Provided limit {limit}is invalid. Please provide a limit >= 5.')

        if condition_function is None:
            self.__nextFunction = self.__defaultNextFunction
        else:
            if not callable(condition_function):
                raise InvalidArgumentError(f'Provided condition function is not a function. Provided type {type(condition_function)}')
            self.condition_function = condition_function
            self.__nextFunction = self.__conditionalNextFunction
    
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.__nextFunction()
    
    def getNextTriple(self):
        if not self.heap:
            raise StopIteration
        
        """
        We use a heap to order the triples by size.
        We use the smallest triple (by c-value) to generate more triples.
        This ensures that the triples are generated in ascending order.
        """
        triple = hq.heappop(self.heap)
        for t in get_triples(triple):
            if t[0] <= self.limit:
                hq.heappush(self.heap, t)
        
        return triple

    def __defaultNextFunction(self):
        return self.getNextTriple()
    
    def __conditionalNextFunction(self):
        """
        We skip triples that do not satisfy the condition
        and yield the first triple that does.
        """
        triple = self.getNextTriple()
        valid, value = self.condition_function(triple)
        while not valid:
            triple = self.getNextTriple()
            valid, value = self.condition_function(triple)
        return value