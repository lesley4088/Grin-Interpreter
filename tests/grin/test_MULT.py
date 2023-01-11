import grin
import unittest
import io
import contextlib

class test_MULT(unittest.TestCase):

    def test_with_ints(self):
        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A 1', 'MULT A 2'])))
        while statements.hasNext() == True and statements.endStatement == False:
            currentLine = statements.getCurrentLine()
            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()
            elif currentLine[0].kind == grin.GrinTokenKind.MULT:
                temp = grin.MULT(currentLine, vr)
                statements.endStatement = temp.operating(vr)
                statements.increase_one_index()

        self.assertEqual(vr.variableDict, {'A': 2})
        self.assertEqual(statements.endStatement, False)


    def test_with_floats(self):
        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A 3.5', 'MULT A 12.0'])))
        while statements.hasNext() == True and statements.endStatement == False:
            currentLine = statements.getCurrentLine()
            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()

            elif currentLine[0].kind == grin.GrinTokenKind.MULT:
                temp = grin.MULT(currentLine, vr)
                statements.endStatement = temp.operating(vr)
                statements.increase_one_index()

        self.assertEqual(vr.variableDict, {'A': 42.0})
        self.assertEqual(statements.endStatement, False)


    def test_with_float_int(self):
        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A 12', 'MULT A 3.5'])))
        while statements.hasNext() == True and statements.endStatement == False:
            currentLine = statements.getCurrentLine()
            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()

            elif currentLine[0].kind == grin.GrinTokenKind.MULT:
                temp = grin.MULT(currentLine, vr)
                statements.endStatement = temp.operating(vr)
                statements.increase_one_index()

        self.assertEqual(vr.variableDict, {'A': 42.0})
        self.assertEqual(statements.endStatement, False)


    def test_with_str_int(self):
        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A 3', 'MULT A "Boo"'])))
        while statements.hasNext() == True and statements.endStatement == False:
            currentLine = statements.getCurrentLine()
            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()

            elif currentLine[0].kind == grin.GrinTokenKind.MULT:
                temp = grin.MULT(currentLine, vr)
                statements.endStatement = temp.operating(vr)
                statements.increase_one_index()

        self.assertEqual(vr.variableDict, {'A': 'BooBooBoo'})
        self.assertEqual(statements.endStatement, False)


    def test_with_str_float(self):
        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A "Boo"', 'MULT A 3.0'])))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:
                currentLine = statements.getCurrentLine()
                if currentLine[0].kind == grin.GrinTokenKind.LET:
                    vr.updateVariableDict(currentLine)
                    statements.increase_one_index()

                elif currentLine[0].kind == grin.GrinTokenKind.MULT:
                    temp = grin.MULT(currentLine, vr)
                    statements.endStatement = temp.operating(vr)
                    statements.increase_one_index()

            self.assertEqual(output.getvalue(), "RunTimeError: can't multiply string by non-int of type 'float'\n")
            self.assertEqual(statements.endStatement, True)


    def test_with_strings(self):
        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A "3"', 'MULT A "Boo"'])))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:
                currentLine = statements.getCurrentLine()
                if currentLine[0].kind == grin.GrinTokenKind.LET:
                    vr.updateVariableDict(currentLine)
                    statements.increase_one_index()

                elif currentLine[0].kind == grin.GrinTokenKind.MULT:
                    temp = grin.MULT(currentLine, vr)
                    statements.endStatement = temp.operating(vr)
                    statements.increase_one_index()

            self.assertEqual(output.getvalue(), "RunTimeError: can't multiply string by non-int of type 'str'\n")
            self.assertEqual(statements.endStatement, True)


    def test_with_identifier(self):
        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A "3"', 'LET B "3.0"', 'MULT A B'])))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:
                currentLine = statements.getCurrentLine()
                if currentLine[0].kind == grin.GrinTokenKind.LET:
                    vr.updateVariableDict(currentLine)
                    statements.increase_one_index()

                elif currentLine[0].kind == grin.GrinTokenKind.MULT:
                    temp = grin.MULT(currentLine, vr)
                    statements.endStatement = temp.operating(vr)
                    statements.increase_one_index()

            self.assertEqual(output.getvalue(), "RunTimeError: can't multiply string by non-int of type 'str'\n")
            self.assertEqual(statements.endStatement, True)