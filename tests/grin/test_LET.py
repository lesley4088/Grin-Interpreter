import unittest
import grin
from grin.LET import *

class test_LET(unittest.TestCase):

    def test_updateVariableDict(self):
        vr = AssignVariables()
        statement = ['LET A 1', 'LET B 2.2', 'LET C "aba"', 'LET D C']
        tokens = list(grin.parse(statement))
        for token in tokens:
            vr.updateVariableDict(token)

        self.assertEqual(vr.variableDict, {'A': 1, 'B': 2.2, 'C': 'aba', 'D': 'aba'})
