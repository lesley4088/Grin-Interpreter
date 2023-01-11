import unittest
import io
import contextlib

import grin


class test_INSTR(unittest.TestCase):

    def test_string_with_empty_str(self):
        vr = grin.AssignVariables()
        command_list = list(grin.parse(['PRINT "STR:"', 'INSTR X', 'PRINT X']))
        statements = grin.EXECUTION(command_list)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:
                currentLine = statements.getCurrentLine()
                if currentLine[0].kind == grin.GrinTokenKind.PRINT:
                    grin.PRINT(currentLine, vr.variableDict)
                    statements.increase_one_index()
                elif currentLine[0].kind == grin.GrinTokenKind.INSTR:
                    grin.INSTR(currentLine, vr)
                    statements.increase_one_index()

            self.assertEqual(output.getvalue(), 'STR:\n\n')
            self.assertEqual(vr.variableDict, {'X': ''})


    def test_string_with_quotation_mark(self):
        vr = grin.AssignVariables()
        command_list = list(grin.parse(['PRINT "STR:"', 'INSTR X', 'PRINT X']))
        statements = grin.EXECUTION(command_list)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:
                currentLine = statements.getCurrentLine()
                if currentLine[0].kind == grin.GrinTokenKind.PRINT:
                    grin.PRINT(currentLine, vr.variableDict)
                    statements.increase_one_index()
                elif currentLine[0].kind == grin.GrinTokenKind.INSTR:
                    grin.INSTR(currentLine, vr)
                    statements.increase_one_index()

            self.assertEqual(output.getvalue(), 'STR:\n"wfnowf"\n')
            self.assertEqual(vr.variableDict, {'X': '"wfnowf"'})

