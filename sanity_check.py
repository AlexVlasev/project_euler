from helpers.errors import InvalidArgumentError


def checkCheckers():
    from helpers.checkers import isPalindrome, isPandigital

    assert not isPalindrome(-121)
    assert isPalindrome('-1--1-')
    assert isPalindrome('-1-1-')
    assert isPalindrome('')

    assert not isPandigital('1234')
    try:
        assert not isPandigital('', min_digit=0, max_digit=-1)
    except InvalidArgumentError:
        pass
    assert isPandigital('-1234567', min_digit=1, max_digit=6)
    assert isPandigital(123.4567809)

def checkIteration():
    from helpers.iteration import PPTIterator

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

def checkNumberTheory():
    from helpers.number_theory import getFactorizations
    from helpers.iteration import product

    factorizations = getFactorizations(1000)
    for n, factors in enumerate(factorizations):
        nn = product(pow(prime, power) for prime, power in factors.items())
        if n > 0 and n != nn:
            print(n, nn, factors)

def checkPartitionFunction():
    from helpers.partition_fxn import Partitions

    partitions_class = Partitions([1, 2], True)
    parts = partitions_class.partitions(5)
    for p in parts:
        print(p)

    partitions_class = Partitions([1, 2, 3, 5], True)
    parts = partitions_class.partitions(10)
    for p in parts:
        print(p)


checkCheckers()
checkIteration()
checkNumberTheory()
checkPartitionFunction()

print('\nSUCCESS!')