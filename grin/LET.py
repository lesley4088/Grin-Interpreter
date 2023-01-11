import grin

class AssignVariables:

    def __init__(self):
        self.variableDict = {}

    def updateVariableDict(self, tokens):
        self._identifier = tokens[1].value

        if tokens[2].kind == grin.GrinTokenKind.IDENTIFIER:
            try:
                value = self.variableDict[tokens[2].text]
                self._value = value
            except KeyError:
                self._value = 0

        else:
            self._value = tokens[2].value
        self.variableDict[self._identifier] = self._value
