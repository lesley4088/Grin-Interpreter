import grin

class IF:

    def __init__(self, tokens, dict):
        if tokens[3].kind == grin.GrinTokenKind.IDENTIFIER:
            try:
                self.value1 = dict[tokens[3].text]
            except KeyError:
                self.value1 = 0
        else:
            self.value1 = tokens[3].value

        self.operator = tokens[4].text

        if tokens[5].kind == grin.GrinTokenKind.IDENTIFIER:
            try:
                self.value2 = dict[tokens[5].text]
            except KeyError:
                self.value1 = 0
        else:
            self.value2 = tokens[5].value


    def compare(self):
        n = None

        if (type(self.value1) is str and type(self.value2) is not str) or \
                (type(self.value2) is str and type(self.value1) is not str):
            print("RunTimeError: relational operators are not supported between 'str' and 'int' or 'str' and 'float'.")
            return None


        if self.operator == '<':
            n = self.value1 < self.value2

        elif self.operator == '>':
            n = self.value1 > self.value2

        elif self.operator == '=':
            n = self.value1 == self.value2

        elif self.operator == '<=':
            n = self.value1 < self.value2

        elif self.operator == '>=':
            n = self.value1 > self.value2

        elif self.operator == '<>':
            n = self.value1 != self.value2

        return n
