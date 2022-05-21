def isPalindrome(number):
    string = str(number)
    bound = int(len(string)/2)
    for i in range(bound):
        if string[i] != string[-1-i]:
            return False
    return True

def isPandigital(number, min_digit=0, max_digit=9):
    if type(number) is int:
        string = str(number)
    else:
        string = number
    digits = set(map(int, string))
    for k in range(min_digit, max_digit + 1):
        if k not in digits:
            return False
    return True