import logging


NUMBERS = '(0|1|2|3|4|5|6|7|8|9)'
LOWER = '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)'
UPPER = '(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)'
LETTERS = '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|' \
          's|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)'
ALPHANUM = '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|' \
          's|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z' \
           '0|1|2|3|4|5|6|7|8|9)'
SYMBOLS = '(!||£|$|%|^|&|*|(|)|_|-|=|+|#|~|;|:|@|<|>|/)'

ALL = 'a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|' \
      's|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z' \
      '0|1|2|3|4|5|6|7|8|9|!||£|$|%|^|&|*|(|)|_|-|=|+|#|~|;|:|@|<|>|/'


class Preprocessor:
    # Handles the special escape sequences \w (any letter) and \d (any numeral)
    # also expands the expressions [0-9], [a-z], [A-Z], [a-zA-Z0-9]

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.length = len(text)

    def replace_special_symbols(self):

        self.text = self.text.replace('[a-z]', LOWER).replace('[A-Z]', UPPER).replace('[0-9]', NUMBERS)
        self.text = self.text.replace('[a-zA-Z0-9]', ALPHANUM)
        self.text = self.text.replace('\w', LETTERS).replace('\d', NUMBERS).replace('\s', ' |   ')

    def handle_alternatives(self):

        while '[' in self.text:

            # Expands expressions of type [abc] into alternation operator
            # expressions of type (a|b|c)

            if self.text.find('[') > self.text.find(']'):
                logging.error("Missing matched parenthesis in alternation expression")
                raise ValueError

            full_el = self.text[self.text.find('['):   self.text.find(']') + 1]
            altern = ''
            for char in full_el[1:-1]:
                altern += char + '|'
            self.text = self.text.replace(full_el, '(' + altern.rstrip('|') + ')')

    def handle_range(self):

        while '/' in self.text:

            # Expands range expressions, does not support nested ranges
            # syntax: /expr()[lower_range:higher_range]/

            beginning_index = self.text.find('/') + 1
            end_index = beginning_index + self.text[beginning_index:].find('/')

            if end_index == -1:
                logging.error("Did not find matching / in range expression")
                raise SyntaxError

            statement = self.text[beginning_index - 1: end_index + 1]
            expression = statement[1:statement.find('[')]  # expression to be repeated
            range_ = statement[statement.find('[') + 1: statement.find(']')]

            low_range = int(range_[0: range_.find(':')])
            high_range = int(range_[range_.find(':') + 1:])

            range_statement = ""
            for i in range(low_range, high_range + 1):
                range_statement = range_statement + expression * i + '|'

            range_statement = '(' + range_statement.rstrip('|') + ')'
            self.text = self.text.replace(statement, range_statement)

    def check_parentheses(self):
        open_par = ["[", "{", "("]
        closed_par = ["]", "}", ")"]
        stack = []
        for i in self.text:
            if i in open_par:
                stack.append(i)
            elif i in closed_par:
                pos = closed_par.index(i)
                if ((len(stack) > 0) and
                        (open_par[pos] == stack[len(stack) - 1])):
                    stack.pop()
                else:
                    logging.error("Found unbalanced parentheses")
                    raise SyntaxError
        if len(stack) == 0:
            return 1
        else:
            logging.error("Found unbalanced parentheses")
            raise SyntaxError

    def preprocess(self):  # Cannot have ranges and alternatives together
        self.replace_special_symbols()
        self.handle_range()
        self.handle_alternatives()
        self.check_parentheses()

        return self.text
