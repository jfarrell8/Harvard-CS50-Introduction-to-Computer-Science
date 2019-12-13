def lines(a, b):
    """Return lines in both a and b"""
    list_a = a.splitlines()
    list_b = b.splitlines()
    combined = set()
    for s in list_a:
        for s1 in list_b:
            if s == s1:
                combined.add(s1)
    return combined


def sentences(a, b):
    """Return sentences in both a and b"""
    from nltk.tokenize import sent_tokenize

    list_a = sent_tokenize(a)
    list_b = sent_tokenize(b)
    combined = set()
    for s in list_a:
        for s1 in list_b:
            if s == s1:
                combined.add(s1)
    return combined

def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    list_a = []
    list_b = []
    combined = set()

    for i in range(len(a) - n + 1):
        list_a.append(a[i:n+i])


    for j in range(len(b) - n + 1):
        list_b.append(b[j:n+j])


    for s in list_a:
        for s1 in list_b:
            if s == s1:
                combined.add(s1)

    return combined
