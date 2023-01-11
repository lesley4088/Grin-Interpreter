import unittest
import io
import contextlib
import grin
class test_PRINT(unittest.TestCase):

    def test_print_identifier(self):
        statements = ['LET A 1', 'PRINT A', 'PRINT B']
        tokens = list(grin.parse(statements))
        tempVR = grin.AssignVariables(tokens[0])
        tempVR.updateVariableDict()
        with contextlib.redirect_stdout(io.StringIO()) as output:
            grin.PRINT(tokens[1], grin.AssignVariables.variableDict)
            grin.PRINT(tokens[2], grin.AssignVariables.variableDict)
            self.assertEqual(output.getvalue(), "1\n0\n")


    def test_print_values(self):
        statements = ['PRINT "A"', 'PRINT 1', 'PRINT 1.1']
        tokens = list(grin.parse(statements))
        with contextlib.redirect_stdout(io.StringIO()) as output:
            grin.PRINT(tokens[0], grin.AssignVariables.variableDict)
            grin.PRINT(tokens[1], grin.AssignVariables.variableDict)
            grin.PRINT(tokens[2], grin.AssignVariables.variableDict)
            self.assertEqual(output.getvalue(), "A\n1\n1.1\n")