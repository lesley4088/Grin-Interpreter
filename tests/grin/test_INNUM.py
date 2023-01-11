import unittest
import io
import contextlib

import grin


class test_INNUM(unittest.TestCase):

    def test_INNUM_with_valid_int(self):
        vr = grin.AssignVariables()
        command_list = list(grin.parse(['PRINT "NUM:"', 'INNUM X', 'PRINT X']))
        statements = grin.EXECUTION(command_list)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:
                currentLine = statements.getCurrentLine()
                if currentLine[0].kind == grin.GrinTokenKind.PRINT:
                    grin.PRINT(currentLine, vr.variableDict)
                    statements.increase_one_index()
                elif currentLine[0].kind == grin.GrinTokenKind.INNUM:
                    statements.endStatement = grin.INNUM(currentLine, vr)
                    statements.increase_one_index()

            self.assertEqual(output.getvalue(), "NUM:\n1\n")
            self.assertEqual(vr.variableDict, {'X': 1})


    def test_INNUM_with_invalid_num(self):
        vr = grin.AssignVariables()
        command_list = list(grin.parse(['PRINT "NUM:"', 'INNUM X', 'PRINT X']))
        statements = grin.EXECUTION(command_list)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:
                currentLine = statements.getCurrentLine()
                if currentLine[0].kind == grin.GrinTokenKind.PRINT:
                    grin.PRINT(currentLine, vr.variableDict)
                    statements.increase_one_index()
                elif currentLine[0].kind == grin.GrinTokenKind.INNUM:
                    statements.endStatement = grin.INNUM(currentLine, vr)
                    statements.increase_one_index()

            self.assertEqual(output.getvalue(), "NUM:\nRunTimeError: please use INSTR to read string.\n")
            self.assertEqual(vr.variableDict, {})


