import grin

class DIV(grin.base_operation):

    def __init__(self, tokens, vr):
        super().__init__(tokens, vr)

    def operating(self, vr):
        identifier = super().getIdentifier()
        value1 = super().getValue1()
        value2 = super().getValue2()

        if type(value1) is int and type(value2) is int:
            vr.variableDict[identifier] = value1 // value2
            return False
        else:
            try:
                vr.variableDict[identifier] = value1 / value2
                return False
            except TypeError:
                if (type(value1) is int and type(value2) is str) or (
                        type(value2) is int and type(value1) is str):
                    print("RunTimeError: unsupported operand type(s) for /: 'str' and 'int'")
                elif (type(value1) is float and type(value2) is str) or (type(value2) is float and type(value1) is str):
                    print("RunTimeError: unsupported operand type(s) for /: 'float' and 'str'")
                elif type(value1) is str and type(value2) is str:
                    print("RunTimeError: unsupported operand type(s) for /: 'str' and 'str'")
                else:
                    print("RunTimeError: unsupported operand type(s) for /")

                return True





