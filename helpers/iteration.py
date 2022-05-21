import heapq as hq

from errors import InvalidArgumentError


def product(iterable, mod=None):
    """
    Multiply a sequence of numbers with optional modding.
    """
    prod = 1
    if mod:
        for x in iterable:
            prod = (prod * x) % mod
    else:
        for x in iterable:
            prod *= x
    return prod

def subsets(iterable):
    _subsets = [[]]
    for e in iterable:
        _new_subsets = [[*s] for s in _subsets]
        _new_subsets.extend([*s, e] for s in _subsets)
        _subsets = _new_subsets
    return _subsets

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
    Triples are generated in increasing c-value. There is an optional stopping condition function.

    You can think of the condition function as making the iterator yield triples only once
    they satisfy the condition. Example in __main__ below.
    """
    def __init__(self, limit, condition_function=None):
        self.limit = limit
        self.heap = [(5, 4, 3)]

        if condition_function is None:
            self.__nextFunction = self.__defaultNextFunction
        else:
            if not callable(condition_function):
                raise InvalidArgumentError(f'Provided condition function is not a function. Provided type {type(condition_function)}')
            self.condition_function = condition_function
            self.__nextFunction = self.__nextWithCondition

    def __iter__(self):
        return self

    def __defaultNextFunction(self):
        return self.getNextTriple()
    
    def __nextWithCondition(self):
        triple = self.getNextTriple()
        valid, value = self.condition_function(triple)
        while not valid:
            triple = self.getNextTriple()
            valid, value = self.condition_function(triple)
        return value
    
    def __next__(self):
        return self.__nextFunction()
    
    def getNextTriple(self):
        if not self.heap:
            raise StopIteration

        triple = hq.heappop(self.heap)
        for t in get_triples(triple):
            if t[0] <= self.limit:
                hq.heappush(self.heap, t)

        return triple

def sumAitken(next_term_function):
    """
    Implementation from Wikipedia.
    """
    x0 = 0                         
    tolerance = pow(10, -12) # desired precision
    epsilon = pow(10, -16) # min division number

    max_iterations = 20
    found_solution = False
    for _ in range(1, max_iterations + 1):
        x1 = next_term_function(x0)
        x2 = next_term_function(x1)

        denominator = (x2 - x1) - (x1 - x0)
        if abs(denominator) < epsilon:
            print('WARNING: denominator is too small')
            break

        aitkenX = x2 - (x2 - x1) ** 2 /denominator
        if abs(aitkenX - x2) < tolerance:
            print("The fixed point is ", aitkenX)
            found_solution = True
            break

        x0 = aitkenX

    if not found_solution:
        print("Warning: Not able to find solution to within the desired tolerance of ", tolerance)
        print("The last computed extrapolate was ", aitkenX)

if __name__ == "__main__":
    def condition(triple):
        c, _, _ = triple
        return c > 98000, triple
    
    iterator = PPTIterator(100000, condition_function=condition)
    for t in iterator:
        print(t)

    for condition in [1, [], {}, IndexError]:
        try:
            iterator = PPTIterator(100000, condition_function=condition)
        except InvalidArgumentError:
            pass

    print('Success!')
