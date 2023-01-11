import grin

class MULT(grin.base_operation):

    def __init__(self, tokens, vr):
        super().__init__(tokens, vr)


    def operating(self, vr):
        identifier = super().getIdentifier()
        value1 = super().getValue1()
        value2 = super().getValue2()

        try:
            vr.variableDict[identifier] = value1 * value2
            return False
        except TypeError:
            if (type(value1) is float and type(value2) is str) or (type(value2) is float and type(value1) is str):
                print("RunTimeError: can't multiply string by non-int of type 'float'")
            elif type(value1) is str and type(value2) is str:
                print("RunTimeError: can't multiply string by non-int of type 'str'")
            else:
                print("RunTimeError: can't multiply sequence by non-int")

            return True

