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
    """
    Obtain the subsets (as lists) of an iterable.
    The items are assumed to be different.
    """
    _subsets = [[]]
    for e in iterable:
        _new_subsets = [[*s] for s in _subsets]
        _new_subsets.extend([*s, e] for s in _subsets)
        _subsets = _new_subsets
    return _subsets

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
