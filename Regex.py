#Regex

#Add the functionality for the DOT operator


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token of type: {type}, value: {value}'.format(
            type=self.type,
            value=repr(self.value)
        )


LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
DOT = 'DOT'
ALT = 'ALT'
STAR = 'STAR'
QMARK = 'QMARK'
PLUS = 'PLUS'
CONCAT = 'CONCAT'
CHAR = 'CHAR'
EOF = 'EOF'


RESERVED_SYMBOLS = {
    '(': 'LPAREN',
    ')': 'RPAREN',
    '.': 'DOT',  # Matches any char
    '|': 'ALT',  # Alternative ex, (a|b)
    '*': 'STAR',  # Arg occurs 0 or more times
    '?': 'QMARK',  # Arg occurs 0 or 1 times
    '+': 'PLUS',  # Arg occurs 1 or more times
    '\\': 'CONCAT',  # Metacharacter (or '\x08')
    'CHAR': 'CHAR',
    'EOF': 'EOF',
}


class Preprocessor:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.length = len(text)

    def preprocess(self):
        numbers = '(0|1|2|3|4|5|6|7|8|9)'
        lower_letters = '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)'
        upper_letters = '(A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)'
        letters = '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|' \
                  's|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z)'

        self.text = self.text.replace('[0-9]', numbers)
        self.text = self.text.replace('[a-z]', lower_letters)
        self.text = self.text.replace('[A-Z]', upper_letters)

        self.text = self.text.replace('\w', letters)
        self.text = self.text.replace('\d', numbers)


        while '[' in self.text: #For choice between elements
            beginning_index = self.text.find('[')
            end_index = self.text.find(']')
            range = self.text[beginning_index:end_index + 1]
            range_string = self.text[beginning_index + 1:end_index]
            alt_string = '('
            for char in range_string:
                alt_string = alt_string + char + '|'
            alt_string = alt_string.rstrip('|') + ')'
            self.text = self.text.replace(range, alt_string)

        return self.text


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.length = len(self.text)

    def get_token(self):
        if self.pos < len(self.text):
            char = self.text[self.pos]
            self.pos += 1

            if char not in RESERVED_SYMBOLS.keys():  # CHAR
                token = Token(CHAR, char)
            else:
                token = Token(RESERVED_SYMBOLS[char], char)
            return token
        else:
            return Token(EOF, '')


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = []
        self.current_token = self.lexer.get_token()

    def eat(self, name):
        if self.current_token.type == name:
            self.current_token = self.lexer.get_token()
        elif self.current_token.type != name:
            print("Expected: ", type, "got: ", self.current_token.type, " damn \n")

    def altern(self):
        self.concat()
        if self.current_token.type == 'ALT':
            token = self.current_token
            self.eat('ALT')
            self.altern()
            self.tokens.append(token)

    def concat(self):
        self.kleene()
        if self.current_token.value not in ')|':
            self.concat()
            self.tokens.append(Token(CONCAT, '\x08'))

    def kleene(self):
        self.primary()
        if self.current_token.type in [STAR, PLUS, QMARK]:
            self.tokens.append(self.current_token)
            self.eat(self.current_token.type)

    def primary(self):
        if self.current_token.type == LPAREN:
            self.eat(LPAREN)
            self.altern()
            self.eat(RPAREN)

        elif self.current_token.type in [CHAR, DOT]:
            self.tokens.append(self.current_token)
            self.eat(self.current_token.type)

        elif self.current_token.type == CONCAT: #Handles the expressions of type \(reserved_symbol)
            self.eat(CONCAT)
            token = self.current_token
            self.eat(token.type)
            token.type = CHAR
            self.tokens.append(token)

    def postfix(self):
        self.altern()
        return self.tokens


class State(object):

    count = 0
    def __init__(self, name=None):
        if name is None:
            name = str(self.count)
            self.__class__.count += 1

        self.name = name
        self.epsilon_transitions = []
        self.transitions = {}
        self.is_end = False
        super().__init__()
        #??????

    def __str__(self):
        f_str = "<Name: {}, transitions = {}, epsilon_transitions = {}>"
        return f_str.format(
            str(self.name),
            repr(self.transitions),
            repr(self.epsilon_transitions)
        )

    def create_transition(self, key, state):
        if key in self.transitions:
            self.transitions[key].append(state)
        else:
            self.transitions[key] = state
            #Creates a list so more than one transition can correspond to one key


class NFA(object):
    def __init__(self, start: State, end: State):
        self.start = start
        self.end = end
        self.current_states = set()
        self.epsilon_states = set()
        end.is_end = True

    def addstate(self, state, state_set):  # add state + recursively add epsilon transitions
        if state in state_set:
            return
        state_set.add(state)
        for eps in state.epsilon_transitions:
            self.addstate(eps, state_set)

    def match(self, string_):
        current_states = set()
        self.addstate(self.start, current_states)
        print("String to match: ", string_)
        for char in string_:
            next_states = set()
            for state in current_states:
                if char in state.transitions.keys():
                    transition_states = state.transitions[char]
                    self.addstate(transition_states, next_states)

            current_states = next_states

        for string_ in current_states:
            if string_.is_end:
                return True
        return False


class NFAbuilder(object):

    def __init__(self, tokens):
        self.tokens = tokens
        self.nfa_stack = []

    def analyse(self):
        for token in self.tokens:
            if token.type is CHAR:
                self.char_nfa(token)
            elif token.type is CONCAT:
                self.concat_nfa()
            elif token.type is QMARK:
                self.qmark_nfa()
            elif token.type is STAR:
                self.star_nfa()
            elif token.type is PLUS:
                self.plus_nfa()
            elif token.type is ALT:
                self.alt_nfa()
        return self.nfa_stack

    def char_nfa(self, token):
        start_state = State()
        end_state = State()
        start_state.create_transition(token.value, end_state)
        end_state.is_end = True
        nfa = NFA(start_state, end_state)
        self.nfa_stack.append(nfa)

    def qmark_nfa(self):
        nfa = self.nfa_stack.pop()
        nfa.start.epsilon_transitions.append(nfa.end)
        self.nfa_stack.append(nfa)

    def star_nfa(self):
        start_state = State()
        end_state = State()
        nfa = self.nfa_stack.pop()

        end_state.is_end = True
        nfa.end.is_end = False

        start_state.epsilon_transitions.append(nfa.start)
        nfa.end.epsilon_transitions.append(nfa.start)
        nfa.end.epsilon_transitions.append(end_state)
        start_state.epsilon_transitions.append(end_state)

        nfa = NFA(start_state, end_state)
        self.nfa_stack.append(nfa)

    def plus_nfa(self):
        start_state = State()
        end_state = State()
        nfa = self.nfa_stack.pop()

        end_state.is_end = True
        nfa.end.is_end = False

        start_state.epsilon_transitions.append(nfa.start)
        nfa.end.epsilon_transitions.append(end_state)
        nfa.end.epsilon_transitions.append(nfa.start)

        nfa = NFA(start_state, end_state)
        self.nfa_stack.append(nfa)

    def concat_nfa(self):
        nfa_second = self.nfa_stack.pop()
        nfa_first = self.nfa_stack.pop()
        nfa_first.end.is_end = False
        nfa_first.end.epsilon_transitions.append(nfa_second.start)

        nfa = NFA(nfa_first.start, nfa_second.end)
        self.nfa_stack.append(nfa)

    def alt_nfa(self):
        nfa_second = self.nfa_stack.pop()
        nfa_first = self.nfa_stack.pop()
        start_state = State()
        end_state = State()

        nfa_first.end.is_end = False
        nfa_second.is_end = False
        end_state.is_end = True

        start_state.epsilon_transitions.append(nfa_first.start)
        start_state.epsilon_transitions.append(nfa_second.start)
        nfa_first.end.epsilon_transitions.append(end_state)
        nfa_second.end.epsilon_transitions.append(end_state)

        nfa = NFA(start_state, end_state)
        self.nfa_stack.append(nfa)


class Compiler:
    def __init__(self, pattern):
        self.pattern = pattern

    def compile(self):
        preprocessor = Preprocessor(self.pattern)
        self.pattern = preprocessor.preprocess()
        lexer = Lexer(self.pattern)
        parser = Parser(lexer)
        postfix_pattern = parser.postfix()

        nfa_stack = NFAbuilder(postfix_pattern).analyse()
        if len(nfa_stack) != 1:
            print("Error")

        automaton = nfa_stack[0]

        return automaton


def main():

    pattern = "abc*d(a|s|d)"
    print("Pattern: ", pattern)


    compiler = Compiler(pattern)
    automaton = compiler.compile()

    match = automaton.match("abcccccccccds")
    print(match)


if __name__ == '__main__':
    main()
