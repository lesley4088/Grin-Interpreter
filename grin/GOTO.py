import grin

class GOTO:

    def __init__(self, token, variableDict):
        if token.kind == grin.GrinTokenKind.IDENTIFIER:
            key = token.value
            try:
                self._target = variableDict[key]
            except KeyError:
                self._target = 0
        elif token.kind == grin.GrinTokenKind.LITERAL_INTEGER:
            self._target = token.value
        elif token.kind == grin.GrinTokenKind.LITERAL_STRING:
            self._target = token.value
        else:
            self._target = None


    def check_if(self, tokens, variableDict):
        temp = grin.IF(tokens, variableDict)
        x = temp.compare()
        return x



    def change_next_line(self, execution, labelDict):
        if self._target == None:
            execution.endStatement = True
            print("RunTimeError: label only accepts int, str and identifier type.")
            return

        if type(self._target) is int:
            if self._target == 0:
                execution.endStatement = True
                print("RunTimeError: infinite loop.")
            elif execution.currentLine + self._target == len(execution.lines):
                execution.endStatement = True
            elif execution.currentLine + self._target not in range(len(execution.lines) + 1):
                execution.endStatement = True
                print("RunTimeError: jumping to a line that's out of range")
            else:
                execution.currentLine += self._target
        elif type(self._target) is str:
            try:
                label = self._target
                execution.currentLine = labelDict[label]
            except KeyError:
                execution.endStatement = True
                print("RunTimeError: jumping to a non-existed label.")

