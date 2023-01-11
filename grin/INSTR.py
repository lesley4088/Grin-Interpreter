import grin

def INSTR(tokens, vr):
    key  = tokens[1].text
    value = input()
    if '\n' in value:
        vr.variableDict[key] = value[:len(value) - 1]
    else:
        vr.variableDict[key] = value