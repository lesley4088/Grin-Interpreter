import grin

class base_operation:

      def __init__(self, tokens, vr):
            self._identifier = tokens[1].text
            try:
                  self._value1 = vr.variableDict[self._identifier]
            except KeyError:
                  self._value1 = 0

            if tokens[2].kind == grin.GrinTokenKind.IDENTIFIER:
                  try:
                        self._value2 = vr.variableDict[tokens[2].text]
                  except KeyError:
                        self._value2 = 0
            else:
                  self._value2 = tokens[2].value


      def getValue1(self):
            return self._value1


      def getValue2(self):
            return self._value2


      def getIdentifier(self):
            return self._identifier