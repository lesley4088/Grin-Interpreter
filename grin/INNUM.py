import grin

def INNUM(tokens, vr):
    key = tokens[1].text
    value = input()
    value = value.strip()
    if '.' in list(value):
        try:
            value = float(value)
            vr.variableDict[key] = value
            return False
        except ValueError:
            print("RunTimeError: please use INSTR to read string.")
            return True
    else:
        try:
            value = int(value)
            vr.variableDict[key] = value
            return False
        except ValueError:
            print("RunTimeError: please use INSTR to read string.")
            return True



