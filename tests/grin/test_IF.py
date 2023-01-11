import unittest
import io
import contextlib

import grin


class test_IF(unittest.TestCase):

    def test_init(self):
        tokens = list(grin.parse(['GOTO 2 IF A > 1']))
        temp = grin.IF(tokens[0], {})
        x = temp.compare()
        self.assertEqual(x, False)
        self.assertEqual(temp.value1, 0)
        self.assertEqual(temp.operator, '>')
        self.assertEqual(temp.value2, 1)


    def test_unsupported_compare_values(self):
        tokens = list(grin.parse(['GOTO 2 IF "" > 1']))
        temp = grin.IF(tokens[0], {})
        with contextlib.redirect_stdout(io.StringIO()) as output:
            x = temp.compare()
            self.assertEqual(x, None)
            self.assertEqual(output.getvalue(), "RunTimeError: relational operators are not supported between 'str' and 'int' or 'str' and 'float'.\n")


    def test_with_identifier(self):
        statements = grin.EXECUTION(list(grin.parse(['LET A 2', 'GOTO A IF A < 3', 'LET B 3', 'LET A 4'])))
        vr = grin.AssignVariables()
        while statements.hasNext() == True and statements.endStatement == False:
            currentLine = statements.getCurrentLine()
            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()
            elif currentLine[0].kind == grin.GrinTokenKind.GOTO:
                temp = grin.GOTO(currentLine[1], vr.variableDict)
                willJump = temp.check_if(currentLine, vr.variableDict)
                if willJump == True:
                    temp.change_next_line(statements, {})
                elif willJump == False:
                    statements.increase_one_index()
                elif willJump == None:
                    statements.endStatement = True
        self.assertEqual(statements.endStatement, False)
        self.assertEqual(vr.variableDict, {'A': 4})


    def test_with_identifier_wrong_type(self):
        statements = grin.EXECUTION(list(grin.parse(['LET A "123"', 'GOTO A IF A < 3', 'LET B 3', 'LET A 4'])))
        vr = grin.AssignVariables()
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:
                currentLine = statements.getCurrentLine()
                if currentLine[0].kind == grin.GrinTokenKind.LET:
                    vr.updateVariableDict(currentLine)
                    statements.increase_one_index()
                elif currentLine[0].kind == grin.GrinTokenKind.GOTO:
                    temp = grin.GOTO(currentLine[1], vr.variableDict)
                    willJump = temp.check_if(currentLine, vr.variableDict)
                    if willJump == True:
                        temp.change_next_line(statements, {})
                    elif willJump == False:
                        statements.increase_one_index()
                    elif willJump == None:
                        statements.endStatement = True
            self.assertEqual(statements.endStatement, True)
            self.assertEqual(output.getvalue(),
                             "RunTimeError: relational operators are not supported between 'str' and 'int' or 'str' and 'float'.\n")
