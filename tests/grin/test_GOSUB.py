import unittest
import io
import contextlib

import grin


class test_GOSUB(unittest.TestCase):

    def test_check_if_return_false(self):
        statements = grin.EXECUTION(
            list(grin.parse(['LET A 3', 'GOSUB A IF A < 3', 'LET B "3"', 'LET A 4'])))
        vr = grin.AssignVariables()
        returnTo = []
        while statements.hasNext() == True and statements.endStatement == False:
            currentLine = statements.getCurrentLine()
            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()
            elif currentLine[0].kind == grin.GrinTokenKind.GOSUB:
                temp = grin.GOSUB(currentLine[1], vr.variableDict, statements)
                willJump = temp.check_if(currentLine, vr.variableDict)
                if willJump == True:
                    temp.change_next_line(statements, {})
                    temp.record_jump_back_line(returnTo)
                elif willJump == False:
                    statements.increase_one_index()
                elif willJump == None:
                    statements.endStatement = True
        self.assertEqual(returnTo, [])
        self.assertEqual(statements.endStatement, False)
        self.assertEqual(vr.variableDict, {'A': 4, 'B':"3"})


    def test_check_if_return_True(self):
        statements = grin.EXECUTION(
            list(grin.parse(['LET C 3', 'GOSUB C IF C = 3.0', 'LET B "3"', 'LET A 4'])))
        vr = grin.AssignVariables()
        returnTo = []
        while statements.hasNext() == True and statements.endStatement == False:
            currentLine = statements.getCurrentLine()
            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()
            elif currentLine[0].kind == grin.GrinTokenKind.GOSUB:
                temp = grin.GOSUB(currentLine[1], vr.variableDict, statements)
                willJump = temp.check_if(currentLine, vr.variableDict)
                if willJump == True:
                    temp.change_next_line(statements, {})
                    temp.record_jump_back_line(returnTo)
                elif willJump == False:
                    statements.increase_one_index()
                elif willJump == None:
                    statements.endStatement = True
        self.assertEqual(returnTo[0].jump_back_line, 2)
        self.assertEqual(statements.endStatement, True)
        self.assertEqual(vr.variableDict, {'C': 3})


    def test_check_if_return_None(self):
        statements = grin.EXECUTION(
            list(grin.parse(['LET C "Boo"', 'GOSUB C IF C = 3.0', 'LET B 3', 'Boo: LET A 4'])))
        vr = grin.AssignVariables()
        returnTo = []
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:
                currentLine = statements.getCurrentLine()
                if currentLine[0].kind == grin.GrinTokenKind.LET:
                    vr.updateVariableDict(currentLine)
                    statements.increase_one_index()
                elif currentLine[0].kind == grin.GrinTokenKind.GOSUB:
                    temp = grin.GOSUB(currentLine[1], vr.variableDict, statements)
                    willJump = temp.check_if(currentLine, vr.variableDict)
                    if willJump == True:
                        temp.change_next_line(statements, {})
                        temp.record_jump_back_line(returnTo)
                    elif willJump == False:
                        statements.increase_one_index()
                    elif willJump == None:
                        statements.endStatement = True
            self.assertEqual(returnTo, [])
            self.assertEqual(statements.endStatement, True)
            self.assertEqual(output.getvalue(),
                             "RunTimeError: relational operators are not supported between 'str' and 'int' or 'str' and 'float'.\n")

    def test_RETURN_with_no_previous_GOSUB(self):
        statements = grin.EXECUTION(
            list(grin.parse(['LET C "Boo"', 'RETURN', 'LET B 3', 'Boo: LET A 4'])))
        vr = grin.AssignVariables()
        returnTo = []
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:
                currentLine = statements.getCurrentLine()
                if currentLine[0].kind == grin.GrinTokenKind.LET:
                    vr.updateVariableDict(currentLine)
                    statements.increase_one_index()
                elif currentLine[0].kind == grin.GrinTokenKind.GOSUB:
                    temp = grin.GOSUB(currentLine[1], vr.variableDict, statements)
                    willJump = temp.check_if(currentLine, vr.variableDict)
                    if willJump == True:
                        temp.change_next_line(statements, {})
                        temp.record_jump_back_line(returnTo)
                    elif willJump == False:
                        statements.increase_one_index()
                    elif willJump == None:
                        statements.endStatement = True
                elif currentLine[0].kind == grin.GrinTokenKind.RETURN:
                    grin.GOSUB.RETURN(returnTo, statements)
            self.assertEqual(returnTo, [])
            self.assertEqual(statements.endStatement, True)
            self.assertEqual(output.getvalue(),"RuntimeError: no previous GOSUB\n")


    def test_RETURN_exactly_end(self):
        statements = grin.EXECUTION(
            list(grin.parse(['LET A 1', 'GOSUB 3', 'LET A 2', 'RETURN', 'GOSUB -2'])))
        vr = grin.AssignVariables()
        returnTo = []

        while statements.hasNext() == True and statements.endStatement == False:
            currentLine = statements.getCurrentLine()
            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()
            elif currentLine[0].kind == grin.GrinTokenKind.GOSUB:
                temp = grin.GOSUB(currentLine[1], vr.variableDict, statements)
                if len(currentLine) > 2:
                    willJump = temp.check_if(currentLine, vr.variableDict)
                    if willJump == True:
                        temp.change_next_line(statements, {})
                        temp.record_jump_back_line(returnTo)
                    elif willJump == False:
                        statements.increase_one_index()
                    elif willJump == None:
                        statements.endStatement = True
                else:
                    temp.change_next_line(statements, {})
                    temp.record_jump_back_line(returnTo)
            elif currentLine[0].kind == grin.GrinTokenKind.RETURN:
                grin.GOSUB.RETURN(returnTo, statements)

        self.assertEqual(vr.variableDict, {'A': 2})
        self.assertEqual(statements.endStatement, False)

    def test_RETURN_guide_example(self):
        statements = grin.EXECUTION(
            list(grin.parse(['LET A 1', 'GOSUB 5', 'PRINT A ', 'END', 'LET A 3', 'RETURN', 'PRINT A', 'LET A 2', 'GOSUB -4', 'PRINT A', 'RETURN'])))
        vr = grin.AssignVariables()
        returnTo = []
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:
                currentLine = statements.getCurrentLine()
                if currentLine[0].kind == grin.GrinTokenKind.LET:
                    vr.updateVariableDict(currentLine)
                    statements.increase_one_index()

                elif currentLine[0].kind == grin.GrinTokenKind.GOSUB:
                    temp = grin.GOSUB(currentLine[1], vr.variableDict, statements)
                    if len(currentLine) > 2:
                        willJump = temp.check_if(currentLine, vr.variableDict)
                        if willJump == True:
                            temp.change_next_line(statements, {})
                            temp.record_jump_back_line(returnTo)
                        elif willJump == False:
                            statements.increase_one_index()
                        elif willJump == None:
                            statements.endStatement = True
                    else:
                        temp.change_next_line(statements, {})
                        temp.record_jump_back_line(returnTo)

                elif currentLine[0].kind == grin.GrinTokenKind.RETURN:
                    grin.GOSUB.RETURN(returnTo, statements)

                elif currentLine[0].kind == grin.GrinTokenKind.END:
                    break

                elif currentLine[0].kind == grin.GrinTokenKind.PRINT:
                    grin.PRINT(currentLine, vr.variableDict)
                    statements.increase_one_index()

            self.assertEqual(output.getvalue(), "1\n3\n3\n")
            self.assertEqual(statements.endStatement, False)
