def captureParser(pattern):
    '''
    splits the regex pattern using { and } as delimiters,
    returns the list of separated strings which include the
    delimiters
    '''
    strings = []
    buffer = ""
    for char in pattern:
        print(buffer)
        if char not in ('{', '}'):
            buffer += char
        else:
            if buffer is not "":
                strings.append(buffer)
            strings.append(char)
            buffer = ""

    if buffer is not "":
        strings.append(buffer)

    strings = list(filter(None, strings))

    return strings

