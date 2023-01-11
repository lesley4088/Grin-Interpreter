import grin


class EXECUTION:

    def __init__(self, command_list):
        self.lines = command_list
        self.currentLine = 0
        self.endStatement = False


    def hasNext(self):
        return self.currentLine < len(self.lines)


    def getCurrentLine(self):
        return self.lines[self.currentLine]


    def increase_one_index(self):
        self.currentLine += 1


    def label_record(self, dict):
        for i in range(len(self.lines)):
            if self.lines[i][0].kind == grin.GrinTokenKind.IDENTIFIER\
                    and self.lines[i][1].kind == grin.GrinTokenKind.COLON:

                try:
                    x = dict[self.lines[i][0].value]
                except KeyError:
                    dict[self.lines[i][0].value] = i

                self.lines[i] = self.lines[i][2:]



def execute_command(command_list):
    statements = grin.EXECUTION(command_list)
    vr = grin.AssignVariables()
    labels = {}
    statements.label_record(labels)
    returnTo = []

    while statements.hasNext() == True and statements.endStatement == False:
        currentLine = statements.getCurrentLine()

        if currentLine[0].kind == grin.GrinTokenKind.LET:
            vr.updateVariableDict(currentLine)
            statements.increase_one_index()

        elif currentLine[0].kind == grin.GrinTokenKind.PRINT:
            grin.PRINT(currentLine, vr.variableDict)
            statements.increase_one_index()

        elif currentLine[0].kind == grin.GrinTokenKind.GOTO:
            temp = grin.GOTO(currentLine[1], vr.variableDict)
            if len(currentLine) > 2:
                willJump = temp.check_if(currentLine, vr.variableDict)
                if willJump == True:
                    temp.change_next_line(statements, labels)
                elif willJump == False:
                    statements.increase_one_index()
                elif willJump == None:
                    statements.endStatement = True
            else:
                temp.change_next_line(statements, labels)


        elif currentLine[0].kind == grin.GrinTokenKind.GOSUB:
            temp = grin.GOSUB(currentLine[1], vr.variableDict, statements)
            if len(currentLine) > 2:
                willJump = temp.check_if(currentLine, vr.variableDict)
                if willJump == True:
                    temp.change_next_line(statements, labels)
                    temp.record_jump_back_line(returnTo)
                elif willJump == False:
                    statements.increase_one_index()
                elif willJump == None:
                    statements.endStatement = True
            else:
                temp.change_next_line(statements, labels)
                temp.record_jump_back_line(returnTo)

        elif currentLine[0].kind == grin.GrinTokenKind.RETURN:
            grin.GOSUB.RETURN(returnTo, statements)

        elif currentLine[0].kind == grin.GrinTokenKind.END:
            return

        elif currentLine[0].kind == grin.GrinTokenKind.INNUM:
            statements.endStatement = grin.INNUM(currentLine, vr)
            statements.increase_one_index()

        elif currentLine[0].kind == grin.GrinTokenKind.INSTR:
            grin.INSTR(currentLine, vr)
            statements.increase_one_index()

        elif currentLine[0].kind == grin.GrinTokenKind.ADD:
            temp = grin.ADD(currentLine, vr)
            statements.endStatement = temp.operating(vr)
            statements.increase_one_index()


        elif currentLine[0].kind == grin.GrinTokenKind.SUB:
            temp = grin.SUB(currentLine, vr)
            statements.endStatement = temp.operating(vr)
            statements.increase_one_index()


        elif currentLine[0].kind == grin.GrinTokenKind.MULT:
            temp = grin.MULT(currentLine, vr)
            statements.endStatement = temp.operating(vr)
            statements.increase_one_index()

        elif currentLine[0].kind == grin.GrinTokenKind.DIV:
            temp = grin.DIV(currentLine, vr)
            statements.endStatement = temp.operating(vr)
            statements.increase_one_index()
















