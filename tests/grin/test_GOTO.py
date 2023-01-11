import unittest
import io
import contextlib

import grin


class test_GOTO(unittest.TestCase):

    def test_GOTO_with_valid_num(self):
        vr = grin.AssignVariables()
        commands = list(grin.parse(['LET A 1', 'GOTO 2', 'LET A 2', 'LET B 2']))
        statements = grin.EXECUTION(commands)
        while statements.hasNext() == True and statements.endStatement == False:

            currentLine = statements.getCurrentLine()
            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()
            elif currentLine[0].kind == grin.GrinTokenKind.GOTO:
                temp = grin.GOTO(currentLine[1], vr.variableDict)
                temp.change_next_line(statements, {})

        self.assertEqual(vr.variableDict, {'A': 1, 'B': 2})
        self.assertEqual(statements.endStatement, False)

    def test_GOTO_with_invalid_num(self):
        vr = grin.AssignVariables()
        commands = list(grin.parse(['LET A 1', 'GOTO 4', 'LET A 2', 'LET B 2']))
        statements = grin.EXECUTION(commands)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:

                currentLine = statements.getCurrentLine()
                if currentLine[0].kind == grin.GrinTokenKind.LET:
                    vr.updateVariableDict(currentLine)
                    statements.increase_one_index()
                elif currentLine[0].kind == grin.GrinTokenKind.GOTO:
                    temp = grin.GOTO(currentLine[1], vr.variableDict)
                    temp.change_next_line(statements, {})

            self.assertEqual(output.getvalue(), "RunTimeError: jumping to a line that's out of range\n")
            self.assertEqual(statements.endStatement, True)


    def test_GOTO_with_0(self):
        vr = grin.AssignVariables()
        commands = list(grin.parse(['LET A 1', 'GOTO 0', 'LET A 2', 'LET B 2']))
        statements = grin.EXECUTION(commands)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:

                currentLine = statements.getCurrentLine()
                if currentLine[0].kind == grin.GrinTokenKind.LET:
                    vr.updateVariableDict(currentLine)
                    statements.increase_one_index()
                elif currentLine[0].kind == grin.GrinTokenKind.GOTO:
                    temp = grin.GOTO(currentLine[1], vr.variableDict)
                    temp.change_next_line(statements, {})

            self.assertEqual(output.getvalue(), "RunTimeError: infinite loop.\n")
            self.assertEqual(statements.endStatement, True)


    def test_GOTO_exactly_end(self):
        vr = grin.AssignVariables()
        commands = list(grin.parse(['LET A 1', 'GOTO 3', 'LET A 2', 'LET B 2']))
        statements = grin.EXECUTION(commands)

        while statements.hasNext() == True and statements.endStatement == False:
            currentLine = statements.getCurrentLine()
            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()
            elif currentLine[0].kind == grin.GrinTokenKind.GOTO:
                temp = grin.GOTO(currentLine[1], vr.variableDict)
                temp.change_next_line(statements, {})

        self.assertEqual(statements.endStatement, True)


    def test_GOTO_with_non_existed_string(self):
        vr = grin.AssignVariables()
        commands = list(grin.parse(['LET A 1', 'GOTO "labels2"', 'LET B 2', 'labels: LET A 2']))
        statements = grin.EXECUTION(commands)
        labels = {}
        statements.label_record(labels)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:

                currentLine = statements.getCurrentLine()

                if currentLine[0].kind == grin.GrinTokenKind.LET:
                    vr.updateVariableDict(currentLine)
                    statements.increase_one_index()
                elif currentLine[0].kind == grin.GrinTokenKind.GOTO:
                    temp = grin.GOTO(currentLine[1], vr.variableDict)
                    temp.change_next_line(statements, labels)
            self.assertEqual(output.getvalue(), "RunTimeError: jumping to a non-existed label.\n")
            self.assertEqual(statements.endStatement, True)


    def test_GOTO_with_valid_string(self):
        vr = grin.AssignVariables()
        commands = list(grin.parse(['LET A 1', 'GOTO "labels"', 'LET B 1', 'labels: LET A 2']))
        statements = grin.EXECUTION(commands)
        labels = {}
        statements.label_record(labels)
        while statements.hasNext() == True and statements.endStatement == False:
            currentLine = statements.getCurrentLine()

            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()
            elif currentLine[0].kind == grin.GrinTokenKind.GOTO:
                temp = grin.GOTO(currentLine[1], vr.variableDict)
                temp.change_next_line(statements, labels)

        self.assertEqual(vr.variableDict, {'A': 2})
        self.assertEqual(statements.endStatement, False)


    def test_GOTO_with_undefined_identifier(self):
        vr = grin.AssignVariables()
        commands = list(grin.parse(['LET A 1', 'LET B 2', 'GOTO C', 'labels: LET A 2']))
        statements = grin.EXECUTION(commands)
        with contextlib.redirect_stdout(io.StringIO()) as output:
            while statements.hasNext() == True and statements.endStatement == False:
                currentLine = statements.getCurrentLine()

                if currentLine[0].kind == grin.GrinTokenKind.LET:
                    vr.updateVariableDict(currentLine)
                    statements.increase_one_index()
                elif currentLine[0].kind == grin.GrinTokenKind.GOTO:
                    temp = grin.GOTO(currentLine[1], vr.variableDict)
                    temp.change_next_line(statements, {})

            self.assertEqual(vr.variableDict, {'A': 1, 'B': 2})
            self.assertEqual(statements.endStatement, True)
            self.assertEqual(output.getvalue(), "RunTimeError: infinite loop.\n")


    def test_GOTO_with_identifier_refer_to_num(self):
        vr = grin.AssignVariables()
        commands = list(grin.parse(['LET A 2', 'GOTO A', 'LET B 2', 'labels: LET A 1', 'LET B 2']))
        statements = grin.EXECUTION(commands)
        labels = {}
        statements.label_record(labels)
        while statements.hasNext() == True and statements.endStatement == False:

            currentLine = statements.getCurrentLine()

            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()
            elif currentLine[0].kind == grin.GrinTokenKind.GOTO:
                temp = grin.GOTO(currentLine[1], vr.variableDict)
                temp.change_next_line(statements, labels)

        self.assertEqual(vr.variableDict, {'A': 1, 'B': 2})
        self.assertEqual(statements.endStatement, False)


    def test_GOTO_with_identifier_refer_to_string(self):
        vr = grin.AssignVariables()
        commands = list(grin.parse(['LET A "lab"', 'GOTO A', 'LET B 1', 'lab: LET A 1', 'LET B 2']))
        statements = grin.EXECUTION(commands)
        labels = {}
        statements.label_record(labels)
        while statements.hasNext() == True and statements.endStatement == False:

            currentLine = statements.getCurrentLine()

            if currentLine[0].kind == grin.GrinTokenKind.LET:
                vr.updateVariableDict(currentLine)
                statements.increase_one_index()
            elif currentLine[0].kind == grin.GrinTokenKind.GOTO:
                temp = grin.GOTO(currentLine[1], vr.variableDict)
                temp.change_next_line(statements, labels)

        self.assertEqual(vr.variableDict, {'A': 1, 'B': 2})
        self.assertEqual(statements.endStatement, False)


    def test_check_if_return_false(self):
        statements = grin.EXECUTION(
            list(grin.parse(['LET A 3', 'GOTO A IF A < 3', 'LET B "3"', 'LET A 4'])))
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
        self.assertEqual(vr.variableDict, {'A': 4, 'B':"3"})


    def test_check_if_return_True(self):
        statements = grin.EXECUTION(
            list(grin.parse(['LET C 3', 'GOTO C IF C = 3.0', 'LET B "3"', 'LET A 4'])))
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
        self.assertEqual(statements.endStatement, True)
        self.assertEqual(vr.variableDict, {'C': 3})


    def test_check_if_return_None(self):
        statements = grin.EXECUTION(
            list(grin.parse(['LET C "Boo"', 'GOTO C IF C = 3.0', 'LET B 3', 'Boo: LET A 4'])))
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
                elif currentLine[0].kind == grin.GrinTokenKind.PRINT:
                    grin.PRINT(currentLine, vr.variableDict)
                    statements.increase_one_index()

            self.assertEqual(statements.endStatement, False)
            self.assertEqual(output.getvalue(),
                             "RunTimeError: relational operators are not supported between 'str' and 'int' or 'str' and 'float'.\n")