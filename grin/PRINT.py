import grin

def PRINT(tokens, dict):
    if tokens[1].kind == grin.GrinTokenKind.IDENTIFIER:
        try:
            print(dict[tokens[1].value])
        except KeyError:
            print(0)
    elif tokens[1].kind == grin.GrinTokenKind.LITERAL_STRING\
            or tokens[1].kind == grin.GrinTokenKind.LITERAL_INTEGER\
            or tokens[1].kind == grin.GrinTokenKind.LITERAL_FLOAT:
        print(tokens[1].value)

