def captureParser(pattern):
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

    return strings



print(captureParser("{}asa{sadasd}{asda}ssda{asd}"))