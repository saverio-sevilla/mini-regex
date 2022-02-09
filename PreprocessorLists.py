# Preprocessor lists

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

    '''
    Handles the special escape equences \w (any letter) and \d (any numeral)
    also expands the constructs [0-9], [a-z], [A-Z], [a-zA-Z0-9]
    '''

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.length = len(text)

    def preprocess(self):

        self.text = self.text.replace('[0-9]', NUMBERS)
        self.text = self.text.replace('[a-z]', LOWER)
        self.text = self.text.replace('[A-Z]', UPPER)
        self.text = self.text.replace('[a-zA-Z0-9]', ALPHANUM)
        self.text = self.text.replace('\w', LETTERS)
        self.text = self.text.replace('\d', NUMBERS)
        self.text = self.text.replace('[sym]', SYMBOLS) #Test this

        while '/' in self.text:

            # Expands range expressions found in the pattern string
            # does not support nested ranges
            # syntax: /expr()[lower_range:higher_range]/
            # currently does not support parsing of whitespaces within the range expression

            beginning_index = self.text.find('/') + 1
            end_index = beginning_index + self.text[beginning_index:].find('/')

            statement = self.text[beginning_index - 1: end_index + 1]
            expression = statement[1:statement.find('[')]
            range_ = statement[statement.find('[') + 1:-2]

            low_range = int(range_[0: range_.find(':')])
            high_range = int(range_[range_.find(':') + 1:])

            range_statement = "("

            for i in range(low_range, high_range + 1):
                range_statement = range_statement + expression * i + '|'

            range_statement = range_statement.rstrip('|') + ')'
            self.text = self.text.replace(statement, range_statement)

        while '[' in self.text:

            # Expands expressions of type [abc] into alternation operator
            # expressions of type (a|b|c)
            # Expressions of this type cannot be nested, does not support whitespaces

            beginning_index = self.text.find('[')
            end_index = self.text.find(']')
            elements_plus_parenthesis = self.text[beginning_index:end_index + 1]
            elements = self.text[beginning_index + 1:end_index]
            alt_string = '('
            for char in elements:
                alt_string = alt_string + char + '|'
            alt_string = alt_string.rstrip('|') + ')'
            self.text = self.text.replace(elements_plus_parenthesis, alt_string)

        return self.text

class SyntaxChecker:

    def __init__(self, text):
        self.text = text

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
                    return "Unbalanced"
        if len(stack) == 0:
            return 1
        else:
            return 0