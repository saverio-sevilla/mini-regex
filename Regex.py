# Regex

import logging
from PreprocessorLists import Preprocessor
logging.basicConfig(level=logging.WARNING)


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return 'Token of type: {type}, value: {value}'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return str(self)


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
    # Recursive descent parser, returns the sequence of tokens in
    # postfix order
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = []
        self.current_token = self.lexer.get_token()

    def eat(self, name):
        if self.current_token.type == name:
            self.current_token = self.lexer.get_token()
        elif self.current_token.type != name:
            logging.error("Unexpected token found, expected {type},"
                          " found: {found_type}".format(type=name, found_type=self.current_token.type))

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

        elif self.current_token.type == CONCAT:
            # handles tokens of type \w and \d
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
        self.transitions = {}  # Change dictionary
        self.is_end = False
        super().__init__()

    def __str__(self):
        f_str = "<Name: {}, transitions = {}, epsilon_transitions = {}>"
        return f_str.format(
            str(self.name),
            repr(self.transitions),
            repr(self.epsilon_transitions)
        )

    def __repr__(self):
        return str(self)

    def create_transition(self, key, state):  # Change for new dictionary, use set_key
        if key in self.transitions:
            self.transitions[key].append(state)
        else:
            self.transitions[key] = state


class NFA(object):
    def __init__(self, start: State, end: State):
        self.start = start
        self.end = end
        self.current_states = set()
        self.epsilon_states = set()
        end.is_end = True

    def addstate(self, state, state_set):
        if state in state_set:
            return
        state_set.add(state)
        for eps in state.epsilon_transitions:
            self.addstate(eps, state_set)

    def match_at_beginning(self, string_):
        logging.debug("Called match_at_beginning with string {str}".format(str=string_))
        match_list = []
        for i in range(len(string_) + 1):
            if self.match(string_[0:i]) is True:
                match_list.append(string_[0:i])
        return match_list

    def match_at_end(self, string_):
        logging.debug("Called match_at_end with string {str}".format(str=string_))
        match_list = []
        for i in range(len(string_)):
            if self.match(string_[i:len(string_)]) is True:
                match_list.append(string_[i:len(string_)])
        return match_list

    @staticmethod
    def get_substrings(string_, min_length):
        substrings = [string_[i: j] for i in range(len(string_))
                      for j in range(i + 1, len(string_) + 1) if len(string_[i:j]) >= min_length]
        return substrings

    def match_anywhere(self, string_, min_length=1):
        logging.debug("Called match_anywhere with string {str} and"
                      " min_length of substrings {min_length}".format(str=string_, min_length=min_length))
        match_list = []
        substrings = self.get_substrings(string_, min_length)
        for string_ in substrings:
            if self.match(string_) is True:
                match_list.append(string_)
        if match_list is not None:
            logging.debug("match_anywhere found at least 1 match")
        return match_list

    def match_text(self, text, type_=None):
        logging.debug("Called match_text")
        match_list = []
        if type_ is None:
            for word in text.split():
                if self.match(word) is True:
                    match_list.append(word)
        elif type_ == "any":
            for word in text.split():
                if self.match_anywhere(word) is True:
                    match_list.append(word)
        elif type_ == "end":
            for word in text.split():
                if self.match_at_end(word) is True:
                    match_list.append(word)
        elif type_ == "beginning":
            for word in text.split():
                if self.match_at_beginning(word) is True:
                    match_list.append(word)

        return match_list

    def match(self, string_):
        logging.debug("Called match with string {str}".format(str=string_))
        current_states = set()
        self.addstate(self.start, current_states)
        for char in string_:
            next_states = set()
            for state in current_states:
                if char in state.transitions.keys():
                    transition_states = state.transitions[char]
                    self.addstate(transition_states, next_states)

            current_states = next_states

        for state in current_states:
            if state.is_end:
                logging.debug("Match returned True")
                return True
        logging.debug("Match returned False")
        return False


class NFAbuilder(object):

    def __init__(self, tokens):
        self.tokens = tokens
        self.nfa_stack = []

    def analyse(self):
        for token in self.tokens:
            if token.type is CHAR:
                self.char_nfa(token)
            elif token.type is DOT:
                self.dot_nfa(token)
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

    def dot_nfa(self, token):
        start_state = State()
        end_state = State()
        start_state.epsilon_transitions.append(end_state)
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
        nfa.end.epsilon_transitions.append(nfa.start)
        nfa.end.epsilon_transitions.append(end_state)

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


def regex(pattern, text, mode="standard"):

    if pattern == "":
        if text == "":
            return True
        return False

    if pattern not in ("", "$", "^"):
        if pattern[0] == '^':
            pattern = pattern[1:]
            mode = "start"
        elif pattern[-1] == '$':
            pattern = pattern[:-1]
            mode = "end"

    preprocessor = Preprocessor(pattern)
    pattern = preprocessor.preprocess()
    lexer = Lexer(pattern)
    parser = Parser(lexer)
    postfix_pattern = parser.postfix()

    nfa_stack = NFAbuilder(postfix_pattern).analyse()

    if len(nfa_stack) != 1:
        logging.error("The NFA stack has length other than 1")

    automaton = nfa_stack[0]

    if mode == "standard":
        match = automaton.match(text)
        return match

    elif mode == "start_capture":
        match = automaton.match_at_beginning(text)
        return match

    elif mode == "start":
        match = automaton.match_at_beginning(text)
        if match:
            return True
        else:
            return False

    elif mode == "end":
        match = automaton.match_at_end(text)
        return match

    elif mode == "any":
        match = automaton.match_anywhere(text)
        return match

    elif mode == "words":
        match = automaton.match_text(text)
        return match

def parse_capture(pattern):
    tokens = pattern.replace("{", "\n{\n").replace("}", "\n}\n").split("\n")
    tokens = list(filter(None, tokens))
    logging.debug("Called parse_capture on pattern {ptrn}".format(ptrn=pattern))
    return tokens

def replace_match(pattern, text):
    match = list(regex(pattern, text, "start_capture"))
    if not match:
        logging.warning("Match not found between capture pattern"
                        " {pt} and string {str}".format(pt=pattern, str=str(text)))
        return False
    text = text.replace(match[-1], "", 1)  # Remove the matched string in the text
    logging.debug("Removed captured string from text, updated text: {txt} ".format(txt=str(text)))
    return match[-1], text

def match_capture(pattern, text):
    tmp_text = text
    strings = parse_capture(pattern)
    logging.debug(f"Parsed string: {strings}")
    captures = []

    for index, string in enumerate(strings):
        if strings[index - 1] is '{':
            match, tmp_text = replace_match(string, tmp_text)
            captures.append(match)
        elif string in '{}':
            pass
        else:
            match, tmp_text = replace_match(string, tmp_text)

    return captures


def main():

    my_list = match_capture("{A}{[0-9]*}-{[0-9]*}-{[0-9]*}-23*", "A328-32-67-23333")
    print(my_list)


if __name__ == '__main__':
    main()
