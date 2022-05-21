from pyprimesieve import primes

from .decorators import cached
from .iteration import product


def factorize(number, prime_numbers=None):
    factors = dict()
    current = number
    
    if prime_numbers:
        ps = prime_numbers
    else:
        ps = primes(number + 1)

    for p in ps:
        while current % p == 0 and current != 1:
            current = int(current/p)
            if p not in factors:
                factors[p] = 1
            else:
                factors[p] += 1
        if current == 1:
            break
    return factors

def numberOfDivisors(number):
    factors = factorize(number)
    divisors = 1
    for _, power in factors.items():
        divisors *= power + 1
    return divisors

def sumOfDivisors(number, div_power=1):
    factors = factorize(number)
    total = 1
    for prime, power in factors.items():
        prime_power = prime ** div_power
        total *= int((prime_power ** (power + 1) - 1)/(prime_power - 1))
    return total

@cached
def generalizedPentagonalNumber(k):
    return int(k*(3*k-1)/2)

start = {
    0: 1,
    1: 1,
    2: 2,
    3: 3,
    4: 5,
}

@cached
def partitions(number):
    if number in start:
        return start[number]
    k = 0
    count = 0
    while True:
        k += 1
        g1 = generalizedPentagonalNumber(k)
        if g1 > number:
            break
        count += int((-1)**(k-1)) * partitions(number - g1)
        g2 = generalizedPentagonalNumber(-k)
        if g2 > number:
            continue
        count += int((-1)**(-k-1)) * partitions(number - g2)
    return count

def mod(number, mod=None):
    if mod:
        return number % mod
    else:
        return number

def normalFunction(p, power):
    prime_power = pow(p, power)
    denominator = p - 1
    return int((prime_power - 1) / denominator)

def moddedFunction(p, power, modNumber):
    prime_power = pow(p, power + 1, modNumber)
    denominator = pow(p - 1, -1, modNumber)
    return int((prime_power - 1) / denominator)


SOD_FUNCTIONS = {
    'normal': normalFunction,
    'modded': moddedFunction,
}

class Factorization:
    def __init__(self, factors: dict):
        self.factors = factors
    
    def __pow__(self, exponent):
        for p in self.factors.keys():
            self.factors[p] *= exponent
        return self
    
    def __mul__(self, other):
        for p, power in other.factors.items():
            if p not in self.factors:
                self.factors[p] = 0
            self.factors[p] += power
        return self
    
    def __truediv__(self, other):
        for p, power in other.factors.items():
            if p not in self.factors:
                self.factors[p] = 0
            self.factors[p] -= power
        return self

    def numOfDivisors(self, modNumber=None):
        return product((power + 1 for power in self.factors.values()), mod=modNumber)

    def _choose_sod_function(self, modNumber=None):
        if modNumber:
            return SOD_FUNCTIONS['modded']
        
        def modded(args, modNumber):
            func = SOD_FUNCTIONS['normal']
            result = func(*args, modNumber)
            return result
        
        return modded

    def sumOfDivisors(self, modNumber=None):
        element = self._choose_sod_function(modNumber)
        generator = (element(p, power) for p, power in self.factors.items())
        result = product(generator, modNumber)
        return mod(result, modNumber)
            
    def toProduct(self):
        return product(p ** power for p, power in self.factors.items())

    def isSquareFree(self):
        for power in self.factors.values():
            if power > 1:
                return False
        return True


class FactorizationWithList:
    def __init__(self, powers: list, prime_numbers: list, modNumber=None):
        self.powers = powers
        self.prime_numbers = prime_numbers
        self.length = len(prime_numbers)
        self.modNumber = modNumber
    
    def __pow__(self, exponent):
        for index in range(self.length):
            self.powers[index] *= exponent
        return self
    
    def __mul__(self, other):
        powers = other.powers
        for index in range(self.length):
            self.powers[index] += powers[index]
        return self
    
    def __truediv__(self, other):
        powers = other.powers
        for index in range(self.length):
            self.powers[index] -= powers[index]
        return self

    def numOfDivisors(self, modNumber=None):
        return product((power + 1 for power in self.powers), mod=modNumber)

    def _choose_sod_function(self, modNumber=None):
        if modNumber:
            return SOD_FUNCTIONS['modded']
        
        def modded(args, modNumber):
            func = SOD_FUNCTIONS['normal']
            result = func(*args, modNumber)
            return result
        
        return modded

    def sumOfDivisors(self, modNumber=None):
        element = self._choose_sod_function(modNumber)
        generator = (element(prime, power) for prime, power in zip(self.prime_numbers, self.powers))
        result = product(generator, modNumber)
        return mod(result, modNumber)
            
    def toProduct(self):
        if self.modNumber:
            generator = (pow(prime, power, self.modNumber) for prime, power in zip(self.prime_numbers, self.powers))
            return product(generator, self.modNumber)

    def isSquareFree(self):
        for power in self.powers:
            if power > 1:
                return False
        return True

class PartitionsFromList:
    def __init__(self, array):
        self.array_set = set(array)
        if len(self.array_set) == 0:
            raise Exception("Array supplied to Partitions class must have length > 0")

        self.array = sorted(self.array_set)
        if 0 in self.array_set:
            raise Exception("Zero must not be part of the array")

        self.minimum = array[0]
        self.maximum = array[-1]
    
    @cached
    def partition(self, element, maximum=None):
        # print(element, maximum)
        if maximum is None:
            max_element = self.maximum
        else:
            max_element = maximum
        if element == 0:
            return 1
        if element < self.minimum:
            return 0
        if element == self.minimum:
            return 1
        
        count = 0
        for a in self.array:
            # print(f'{element} -- {a}')
            if a > element or a > max_element:
                break
            count += self.partition(element - a, a)
        # print(element, maximum, count)
        return count

def factorInFactorial(n, p):
    divided = n
    power = 0
    while divided >= p:
        divided /= p
        power += int(divided)
    return power

def factorizeFactorial(n, prime_numbers=None):
    factors = dict()
    primes_in_n = prime_numbers
    if not prime_numbers:
        primes_in_n = primes(n + 1)
    half = n // 2 + 1
    for prime in primes_in_n:
        if prime > n:
            break
        if prime >= half:
            factors[prime] = 1
            continue
        factors[prime] = factorInFactorial(n, prime)
    return factors

def getFactorizations(limit, prime_numbers=None):
    if prime_numbers:
        ps = prime_numbers
    else:
        ps = primes(limit)
    factorizations = [dict() for _ in range(limit)]
    for p in ps:
        multiplied = 1
        power = 0
        while multiplied < limit:
            multiplied *= p
            current = multiplied
            power += 1
            while current < limit:
                factorizations[current][p] = power
                current += multiplied
    return factorizations

def primorial(limit):
    # Product of primes up to limit
    return product(primes(limit))

def primorialPrimes(k, prime_numbers):
    return product(prime_numbers[:k])
