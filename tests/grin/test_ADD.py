import grin
import unittest
import io
import contextlib

class test_ADD(unittest.TestCase):

    def test_with_ints(self):
        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A 1', 'ADD A 2'])))
        while statements.hasNext() == True and statements.endStatement == False:
            currentLine = statements.getCurrentLine()
            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()


            elif currentLine[0].kind == grin.GrinTokenKind.ADD:
                temp = grin.ADD(currentLine, vr)
                statements.endStatement = temp.operating(vr)
                statements.increase_one_index()

        self.assertEqual(vr.variableDict, {'A': 3})
        self.assertEqual(statements.endStatement, False)


    def test_with_floats(self):
        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A 3.3', 'ADD A 2.2'])))
        while statements.hasNext() == True and statements.endStatement == False:
            currentLine = statements.getCurrentLine()
            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()


            elif currentLine[0].kind == grin.GrinTokenKind.ADD:
                temp = grin.ADD(currentLine, vr)
                statements.endStatement = temp.operating(vr)
                statements.increase_one_index()

        self.assertEqual(vr.variableDict, {'A': 5.5})
        self.assertEqual(statements.endStatement, False)


    def test_with_float_int(self):
        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A 3.3', 'ADD A 2'])))
        while statements.hasNext() == True and statements.endStatement == False:
            currentLine = statements.getCurrentLine()
            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()

            elif currentLine[0].kind == grin.GrinTokenKind.ADD:
                temp = grin.ADD(currentLine, vr)
                statements.endStatement = temp.operating(vr)
                statements.increase_one_index()

        self.assertEqual(vr.variableDict, {'A': 5.3})
        self.assertEqual(statements.endStatement, False)


    def test_with_strings(self):
        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A "123"', 'ADD A "45"'])))
        while statements.hasNext() == True and statements.endStatement == False:
            currentLine = statements.getCurrentLine()
            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()

            elif currentLine[0].kind == grin.GrinTokenKind.ADD:
                temp = grin.ADD(currentLine, vr)
                statements.endStatement = temp.operating(vr)
                statements.increase_one_index()

        self.assertEqual(vr.variableDict, {'A': "12345"})
        self.assertEqual(statements.endStatement, False)


    def test_with_str_int(self):
        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A "123"', 'ADD A 45'])))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:
                currentLine = statements.getCurrentLine()
                if currentLine[0].kind == grin.GrinTokenKind.LET:
                    vr.updateVariableDict(currentLine)
                    statements.increase_one_index()

                elif currentLine[0].kind == grin.GrinTokenKind.ADD:
                    temp = grin.ADD(currentLine, vr)
                    statements.endStatement = temp.operating(vr)
                    statements.increase_one_index()

            self.assertEqual(output.getvalue(), "RunTimeError: unsupported operand type(s) for +: 'int' and 'str'\n")
            self.assertEqual(statements.endStatement, True)


    def test_with_str_float(self):
        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A 12.3', 'ADD A "45"'])))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:
                currentLine = statements.getCurrentLine()
                if currentLine[0].kind == grin.GrinTokenKind.LET:
                    vr.updateVariableDict(currentLine)
                    statements.increase_one_index()

                elif currentLine[0].kind == grin.GrinTokenKind.ADD:
                    temp = grin.ADD(currentLine, vr)
                    statements.endStatement = temp.operating(vr)
                    statements.increase_one_index()

            self.assertEqual(output.getvalue(), "RunTimeError: unsupported operand type(s) for +: 'float' and 'str'\n")
            self.assertEqual(statements.endStatement, True)

    def test_with_identifier(self):
        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A "123"', 'ADD A B'])))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:
                currentLine = statements.getCurrentLine()
                if currentLine[0].kind == grin.GrinTokenKind.LET:
                    vr.updateVariableDict(currentLine)
                    statements.increase_one_index()

                elif currentLine[0].kind == grin.GrinTokenKind.ADD:
                    temp = grin.ADD(currentLine, vr)
                    statements.endStatement = temp.operating(vr)
                    statements.increase_one_index()

            self.assertEqual(output.getvalue(),
                             "RunTimeError: unsupported operand type(s) for +: 'int' and 'str'\n")
            self.assertEqual(statements.endStatement, True)

    def test_with_identifier_error(self):
        vr = grin.AssignVariables()
        statements = grin.EXECUTION(list(grin.parse(['LET A 4.5', 'ADD A A'])))
        while statements.hasNext() == True and statements.endStatement == False:
            currentLine = statements.getCurrentLine()
            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()

            elif currentLine[0].kind == grin.GrinTokenKind.ADD:
                temp = grin.ADD(currentLine, vr)
                statements.endStatement = temp.operating(vr)
                statements.increase_one_index()

        self.assertEqual(vr.variableDict, {'A': 9.0})
        self.assertEqual(statements.endStatement, False)