import unittest
from src.Regex import match_capture, RegexBuilder, simple_match


class TestRegex(unittest.TestCase):

    def test_basic(self):
        # basic equalities and limit cases
        self.assertEqual(simple_match("abc", "abc"), True)
        self.assertEqual(simple_match(" ", " "), True)
        self.assertEqual(simple_match("a", "a"), True)
        self.assertEqual(simple_match(" ", ""), False)
        self.assertEqual(simple_match("abc", ""), False)

    def test_operators(self):
        # basic equalities and limit cases
        self.assertEqual(simple_match("a*", "aaa"), True)
        self.assertEqual(simple_match("abc*", "abccccc"), True)
        self.assertEqual(simple_match("abc*", "ab"), True)
        self.assertEqual(simple_match("a*", ""), True)
        # Plus operator
        self.assertEqual(simple_match("a+", "aaaaa"), True)
        self.assertEqual(simple_match("ba+", "b"), False)
        self.assertEqual(simple_match("ba+", "ba"), True)
        # Question operator
        self.assertEqual(simple_match("bac?", "bac"), True)
        self.assertEqual(simple_match("bac?", "ba"), True)
        self.assertEqual(simple_match("bac?", "bacc"), False)
        # Alt operator
        self.assertEqual(simple_match("a(a|b|c)", "ab"), True)
        self.assertEqual(simple_match("(a|b|c)(a|b|c)", "ba"), True)
        self.assertEqual(simple_match("(abc|cba)", "cba"), True)

    def test_match_begin(self):
        # Tests the match at beginning function
        self.assertEqual(simple_match("^abc", "abcd"), True)
        self.assertEqual(simple_match("^123", "12345"), True)
        self.assertEqual(simple_match("^123", "123"), True)
        self.assertEqual(simple_match("^123", "12"), False)
        self.assertEqual(simple_match("^123", "abc"), False)
        self.assertEqual(simple_match("^(a|b|c)(1|2|3)", "a23"), True)

    def text_match_end(self):
        # Tests the match at end function
        self.assertEqual(simple_match("abc$", "1abc"), True)
        self.assertEqual(simple_match("abc$", "abc"), True)
        self.assertEqual(simple_match("abc$", "1abcd"), True)
        self.assertEqual(simple_match("$", "abc"), False)
        self.assertEqual(simple_match("$", ""), False)

    def test_alternation_macro(self):
        # Tests the expansion of the alternative macro ex.[abc]
        self.assertEqual(simple_match("[abcdef]d", "fd"), True)
        self.assertEqual(simple_match("[123][1234][567]d", "247d"), True)
        self.assertEqual(simple_match("[a]d", "ad"), True)

    def test_range_macro(self):
        # Tests the expansion of the range macro
        self.assertEqual(simple_match("/(abc)[2:5]/", "abcabc"), True)
        self.assertEqual(simple_match("/(1)[5:7]/", "11111"), True)
        self.assertEqual(simple_match("/(1)[5:7]/", "11111111"), False)
        self.assertEqual(simple_match("/(1)[5:7]/", "1111"), False)
        self.assertEqual(simple_match("abc/(1)[5:7]/", "abc11111"), True)
        self.assertEqual(simple_match("abc/(1)[5:7]/d", "abc11111d"), True)
        self.assertEqual(simple_match("/(a?)[5:7]/", "aaa"), True)
        self.assertEqual(simple_match("/(abc|abd)[2:3]/", "abdabd"), True)
        self.assertEqual(simple_match("/(abc|abd)[2:3]/", "abcabd"), True)
        self.assertEqual(simple_match("123-/(abc|abd)[2:3]/-567?", "123-abcabdabc-56"), True)

    def test_combination(self):
        # More complex cases
        self.assertEqual(simple_match("a*b*c?(d|e)", "aaabbe"), True)
        self.assertEqual(simple_match("(a|b)*(e|f|g)?", "bbbabbbbbg"), True) # * has higher priority than |
        self.assertEqual(simple_match("(a*|b*)(e|f|g)?", "bbbabbbbbg"), False)
        self.assertEqual(simple_match("((a|b)|(c|d))", "a"), True)

    def test_capture(self):
        # Tests the capture function
        self.assertEqual(match_capture("{A}{[0-9]*}-{[0-9]*}-{[0-9]*}", "A328-32-67"), ['A', '328', '32', '67'])
        self.assertEqual(match_capture("{[a-z]*}-{[a-z]*}", "first-second"), ['first', 'second'])
        self.assertEqual(match_capture("text-{a|b|c}-text", "text-a-text"), ['a'])
        self.assertEqual(match_capture("a*b*{c*}d*", "aaabbbccccccccd"), ['cccccccc'])
        self.assertEqual(match_capture("a{(d|b|c)}{(1|2)}", "ad2"), ['d', '2'])
        self.assertEqual(match_capture("{a?}{b?}{cde*}", "cdeeeee"), ['', '', 'cdeeeee'])
        self.assertEqual(match_capture("{0*}1{0*}", "00000100000"), ['00000', '00000'])

    def test_regexbuilder(self):
        test = RegexBuilder("...")
        matcher = test.build_matcher()
        self.assertEqual(matcher.match("aab"), True)

        test = RegexBuilder("a*b*c?(d|e)")
        matcher = test.build_matcher()
        self.assertEqual(matcher.match("aaabbe"), True)

        test = RegexBuilder("abc$")
        matcher = test.build_matcher()
        self.assertEqual(matcher.match("123abc"), True)



if __name__ == '__main__':
    unittest.main()
