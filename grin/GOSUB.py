import grin

class GOSUB(grin.GOTO):

    def __init__(self, token, variableDict, execution):
        super().__init__(token, variableDict)
        self.jump_back_line = execution.currentLine + 1


    def check_if(self, tokens, variableDict):
        return super().check_if(tokens, variableDict)


    def change_next_line(self, execution, labelDict):
        super().change_next_line(execution, labelDict)

    def record_jump_back_line(self, list):
        list.append(self)

    @staticmethod
    def RETURN(list, execution):
        if list == []:
            print("RuntimeError: no previous GOSUB")
            execution.endStatement = True
        else:
            execution.currentLine = list[-1].jump_back_line
            list.pop()