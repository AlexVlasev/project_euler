class InvalidArgumentError(Exception):
    pass

def isPalindrome(sequence):
    """
    Check if a sequence is a palindrome.
    This accepts 
    """
    if type(sequence) not in (int, float, str):
        raise InvalidArgumentError(f'The sequence type must be one of int, float or str. {type(sequence)} provided.')

    string = str(sequence)
    for i in range(len(string) // 2):
        if string[i] != string[-1-i]:
            return False
    return True

def isPandigital(sequence, min_digit=0, max_digit=9):
    """
    Check to see if a sequence is pandigital, that is
    it includes all digits from min_digit to max_digit.
    This is not limited to 
    """
    if min_digit > max_digit:
        raise InvalidArgumentError('The provided max_digit is too small')
    if type(sequence) not in (int, float, str):
        raise InvalidArgumentError(f'The sequence type must be one of int, float or str. {type(sequence)} provided.')

    digits = set(str(sequence))
    for k in range(min_digit, max_digit + 1):
        if str(k) not in digits:
            return False
    return True

if __name__ == '__main__':
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

    print("Success!")
