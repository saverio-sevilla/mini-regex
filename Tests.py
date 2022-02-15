import unittest
from Regex import regex, match_capture, parse_capture

class TestRegex(unittest.TestCase):

    def test_basic(self):
        # basic equalities and limit cases
        self.assertEqual(regex("abc", "abc"), True)
        self.assertEqual(regex("",""), True)
        self.assertEqual(regex(" "," "), True)
        self.assertEqual(regex("a","a"), True)
        self.assertEqual(regex(" ",""), False)
        self.assertEqual(regex("","abc"), False)
        self.assertEqual(regex("abc",""), False)

    def test_operators(self):
        # basic equalities and limit cases
        self.assertEqual(regex("a*", "aaa"), True)
        self.assertEqual(regex("abc*","abccccc"), True)
        self.assertEqual(regex("abc*","ab"), True)
        self.assertEqual(regex("a*",""), True)
        # Plus operator
        self.assertEqual(regex("a+", "aaaaa"), True)
        self.assertEqual(regex("ba+","b"), False)
        self.assertEqual(regex("ba+","ba"), True)
        # Question operator
        self.assertEqual(regex("bac?", "bac"), True)
        self.assertEqual(regex("bac?","ba"), True)
        self.assertEqual(regex("bac?","bacc"), False)
        # Alt operator
        self.assertEqual(regex("a(a|b|c)", "ab"), True)
        self.assertEqual(regex("(a|b|c)(a|b|c)","ba"), True)
        self.assertEqual(regex("(abc|cba)","cba"), True)

    def test_match_begin(self):
        self.assertEqual(regex("^abc", "abcd"), True)
        self.assertEqual(regex("^123", "12345"), True)
        self.assertEqual(regex("^123", "123"), True)
        self.assertEqual(regex("^123", "12"), False)
        self.assertEqual(regex("^123", "abc"), False)
        self.assertEqual(regex("^", ""), False)
        self.assertEqual(regex("^", " "), False)
        self.assertEqual(regex("^", "abc"), False)
        self.assertEqual(regex("^(a|b|c)(1|2|3)", "a23"), True)

    def text_match_end(self):
        self.assertEqual(regex("abc$", "1abc"), True)
        self.assertEqual(regex("abc$", "abc"), True)
        self.assertEqual(regex("abc$", "1abcd"), True)
        self.assertEqual(regex("$", "abc"), False)
        self.assertEqual(regex("$", ""), False)

    def test_alternation_macro(self):
        self.assertEqual(regex("[abcdef]d", "fd"), True)
        self.assertEqual(regex("[123][1234][567]d", "247d"), True)
        self.assertEqual(regex("[a]d", "ad"), True)

    def test_range_macro(self):
        self.assertEqual(regex("/(abc)[2:5]/", "abcabc"), True)
        self.assertEqual(regex("/(1)[5:7]/", "11111"), True)
        self.assertEqual(regex("/(1)[5:7]/", "11111111"), False)
        self.assertEqual(regex("/(1)[5:7]/", "1111"), False)
        self.assertEqual(regex("abc/(1)[5:7]/", "abc11111"), True)
        self.assertEqual(regex("abc/(1)[5:7]/d", "abc11111d"), True)
        self.assertEqual(regex("/(a?)[5:7]/", "aaa"), True)
        self.assertEqual(regex("/(abc|abd)[2:3]/", "abdabd"), True)
        self.assertEqual(regex("/(abc|abd)[2:3]/", "abcabd"), True)
        self.assertEqual(regex("123-/(abc|abd)[2:3]/-567?", "123-abcabdabc-56"), True)

    def test_combination(self):
        self.assertEqual(regex("a*b*c?(d|e)", "aaabbe"), True)
        self.assertEqual(regex("(a|b)*(e|f|g)?", "bbbabbbbbg"), True) # * has higher priority than |
        self.assertEqual(regex("(a*|b*)(e|f|g)?", "bbbabbbbbg"), False)
        self.assertEqual(regex("((a|b)|(c|d))", "a"), True)

    def test_capture(self):
        self.assertEqual(match_capture("{A}{[0-9]*}-{[0-9]*}-{[0-9]*}", "A328-32-67"), ['A', '328', '32', '67'])
        self.assertEqual(match_capture("{[a-z]*}-{[a-z]*}", "first-second"), ['first', 'second'])
        self.assertEqual(match_capture("text-{a|b|c}-text", "text-a-text"), ['a'])
        self.assertEqual(match_capture("a*b*{c*}d*", "aaabbbccccccccd"), ['cccccccc'])
        self.assertEqual(match_capture("a{(d|b|c)}{(1|2)}", "ad2"), ['d', '2'])
        self.assertEqual(match_capture("{a?}{b?}{cde*}", "cdeeeee"), ['', '', 'cdeeeee'])
        self.assertEqual(match_capture("{0*}1{0*}", "00000100000"), ['00000', '00000'])


if __name__ == '__main__':
    unittest.main()
