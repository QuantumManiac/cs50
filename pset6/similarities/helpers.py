from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    aline = list(a.split('\n'))
    bline = list(b.split('\n'))
    return compare(aline, bline)


def sentences(a, b):
    """Return sentences in both a and b"""

    asent = list(sent_tokenize(a))
    bsent = list(sent_tokenize(b))
    return compare(asent, bsent)


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""

    asub = list(substringhelper(a, n))
    bsub = list(substringhelper(b, n))
    return compare(asub, bsub)


def substringhelper(string, n):

    substring = []
    for i in range(len(string) - n + 1):
        substring.append(string[i:i + n])
    return substring


def compare(a, b):

    output = []
    for i in a:
        for j in b:
            if i == j and i not in output:
                output.append(j)
    return output