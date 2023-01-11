import grin
import unittest
import io
import contextlib

class test_DIV(unittest.TestCase):

    def test_with_ints(self):
        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A 1', 'DIV A 2'])))
        while statements.hasNext() == True and statements.endStatement == False:
            currentLine = statements.getCurrentLine()
            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()

            elif currentLine[0].kind == grin.GrinTokenKind.DIV:
                temp = grin.DIV(currentLine, vr)
                statements.endStatement = temp.operating(vr)
                statements.increase_one_index()

        self.assertEqual(vr.variableDict, {'A': 0})
        self.assertEqual(statements.endStatement, False)


    def test_with_int_float(self):
        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A 4.0', 'DIV A 2'])))
        while statements.hasNext() == True and statements.endStatement == False:
            currentLine = statements.getCurrentLine()
            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()

            elif currentLine[0].kind == grin.GrinTokenKind.DIV:
                temp = grin.DIV(currentLine, vr)
                statements.endStatement = temp.operating(vr)
                statements.increase_one_index()

        self.assertEqual(vr.variableDict, {'A': 2.0})
        self.assertEqual(statements.endStatement, False)


    def test_with_float_int(self):
        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A 4', 'LET B 2.0', 'DIV A B'])))
        while statements.hasNext() == True and statements.endStatement == False:
            currentLine = statements.getCurrentLine()
            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()

            elif currentLine[0].kind == grin.GrinTokenKind.DIV:
                temp = grin.DIV(currentLine, vr)
                statements.endStatement = temp.operating(vr)
                statements.increase_one_index()

        self.assertEqual(vr.variableDict, {'A': 2.0, "B": 2.0})
        self.assertEqual(statements.endStatement, False)


    def test_with_strings(self):

        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A "1"', 'DIV A "2"'])))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:
                currentLine = statements.getCurrentLine()
                if currentLine[0].kind == grin.GrinTokenKind.LET:
                    vr.updateVariableDict(currentLine)
                    statements.increase_one_index()

                elif currentLine[0].kind == grin.GrinTokenKind.DIV:
                    temp = grin.DIV(currentLine, vr)
                    statements.endStatement = temp.operating(vr)
                    statements.increase_one_index()


            self.assertEqual(statements.endStatement, True)
            self.assertEqual(output.getvalue(), "RunTimeError: unsupported operand type(s) for /: 'str' and 'str'\n")


    def test_with_identifier(self):

        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A "1"', 'LET B "2"', 'DIV A B'])))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:
                currentLine = statements.getCurrentLine()
                if currentLine[0].kind == grin.GrinTokenKind.LET:
                    vr.updateVariableDict(currentLine)
                    statements.increase_one_index()

                elif currentLine[0].kind == grin.GrinTokenKind.DIV:
                    temp = grin.DIV(currentLine, vr)
                    statements.endStatement = temp.operating(vr)
                    statements.increase_one_index()


            self.assertEqual(statements.endStatement, True)
            self.assertEqual(output.getvalue(), "RunTimeError: unsupported operand type(s) for /: 'str' and 'str'\n")