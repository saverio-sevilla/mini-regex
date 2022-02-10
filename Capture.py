def capture(pattern):
    tokens = pattern.replace("{", "\n{\n").replace("}", "\n}\n").split("\n")
    tokens = list(filter(None, tokens))
    return tokens

