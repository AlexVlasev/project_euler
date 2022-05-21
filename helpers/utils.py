def getFromFile(filename):
    with open(filename, 'r') as infile:
        lines = map(lambda x: x.strip(), infile.readlines())
        return list(lines)

def twoDecimals(number):
    return int(100 * number) / 100

def printTime(seconds, message):
    print(f'{twoDecimals(seconds)} sec: {message}')

def padLeft(string, length, character):
    padding =  character * (length - len(string))
    return f'{padding}{string}'


def printAnswer(problemNumber, answer):
    print(f'\nP{padLeft(str(problemNumber), 3, "0")}. Answer: {answer}')
