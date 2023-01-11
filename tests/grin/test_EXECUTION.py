import unittest
import grin
class test_EXECUTION(unittest.TestCase):

    def test_label_record(self):
        labels = {}
        commands = list(grin.parse(['manlin: LET A 1', 'manlin: GOTO 2', 'LET A 2', 'zhe: LET B 2']))
        statements = grin.EXECUTION(commands)
        statements.label_record(labels)

        self.assertEqual(labels, {'manlin': 0, 'zhe': 3})

