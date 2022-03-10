# Regex engine 

A small regex engine written in Python to get familiar with NFA, the grammar rules mostly follow the Python regular expression library, with some exceptions. The engine can be used to match a regex pattern to the beginning or end of a string or anywhere inside a given string. 

The basic regex match function is:

```
regex(pattern, text, mode="standard")
```

The possible modes are `standard` which looks for an exact match between the pattern and the string, returning a Boolean, `begin` which matches the regex with the beginning of the string and returns the list of matching strings, `end` which matches with the end of a string and returns the list of matches, `any` which will look for matches between the pattern and every substring, returning a list of matches.

Example:

```
regex("abc*\d", "abccc1)
```
returns `true`

This function can be applied to more complex regex expressions, such as:
```
regex("^(a|b|c)(1|2|3)", "a23")
```
which returns true.

The function:
```
match_capture(pattern, text)
```

attempts to match the pattern with a user provided string passed as the second argument. It returns a list of captured strings, it will
fail with an error message if a suitable match is not found for one of the expressions to capture. Backtracking is not performed.

As an example the calls:
```
match_capture("{A}{[0-9]*}-{[0-9]*}-{[0-9]*}", "A328-32-67"))
```
```
match_capture("{[a-z]*}-{[a-z]*}", "first-second")
```
will return:
```
['A', '328', '32', '67']
```
```
['first', 'second]
```

## Features

###Operators
- * -> match zero or more times  
- + -> match one or more times
- ? -> match zero or one time
- | -> OR operator

###Groups
- [0-9] -> match any digit 
- [a-z] -> match any lower case character
- [A-Z] -> match any upper case character
- [a-zA-Z0-9] -> match any alphanumeric character
- [chars] matches any character in group enclosed by parenthesis, ex. [abcd]
- "." (wildcard) matches any character

###Escapes
- \w -> matches any alphabetic character 
- \d -> matches numeral character
- \s -> matches whitespace

- operators *, +, ?, | from standard regex syntax
- round parentheses to group expressions (ex. (abc)*, (a|b|c) )
- special expressions [0-9], [a-z], [a-zA-Z0-9]
- escape sequences of type backslash plus a reserved character, which will be matches like a literal
- special escape sequences /w (any letter, upper or lowercase), /d (any digit) and [sym] (any symbol) 
- shorthand syntax for alternatives using square parentheses, `[123abc]` will be expanded into `(1|2|3|a|b)`
- ranges with syntax `/(expr)[lower_bound:upper_bound]/` 
