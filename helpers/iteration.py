import heapq as hq

def product(iterable, mod=None):
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
    c, b, a = triple
    a2, b2, c2 = 2 * a, 2 * b, 2 * c
    c3 = 3 * c
    t1 = (-a2 + b2 + c3, -a2 + b + c2, -a + b2 + c2)
    t2 = (a2 - b2 + c3, a2 - b + c2, a - b2 + c2)
    t3 = (a2 + b2 + c3, a2 + b + c2, a + b2 + c2)
    return t1, t2, t3


class PPTIterator:
    def __init__(self, limit, condition=None):
        self.limit = limit
        self.heap = [(5, 4, 3)]
        # self.max_length = 1
        self.condition = condition

    def __iter__(self):
        return self
    
    def __next__(self):
        if not self.condition:
            return self.grab_next()
        
        triple = self.grab_next()
        valid, value = self.condition(triple)
        while not valid:
            triple = self.grab_next()
            valid, value = self.condition(triple)
        return value
    
    def grab_next(self):
        if not self.heap:
            raise StopIteration

        triple = hq.heappop(self.heap)
        for t in get_triples(triple):
            if t[0] <= self.limit:
                hq.heappush(self.heap, t)
        # self.max_length = max(self.max_length, len(self.heap))
        return triple

def sumAitken(next_term_function):
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
        return c > 98000
    
    iterator = PPTIterator(100000, condition=condition)
    for t in iterator:
        print(t)
