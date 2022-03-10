# Regex engine 

A small regex engine written in Python, follow standard regex syntax. The engine can be used to match a regex pattern to the beginning or end of a string or anywhere inside a given string. 

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
fail with an error message if a suitable match is not found for one of the expressions to capture. Backtracking is not performed and the operators are greedy by default.

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

### Operators and quantifiers
All quantifiers are greedy in both the stardard regex mode and the match_capture function, to this moment backtracking is not supported.
- \* -> match zero or more times  
- \+ -> match one or more times
- ? -> match zero or one time
- | -> OR operator
- Ranges (syntax: /(expr)[n:m]/ ) will match the expression between n and m times

### Groups
These constructs help with matching characters which belong to a common type.
- [0-9] -> match any digit 
- [a-z] -> match any lower case character
- [A-Z] -> match any upper case character
- [a-zA-Z0-9] -> match any alphanumeric character
- [chars] matches any character in group enclosed by parenthesis, ex. [abcd]
- "." (wildcard) matches any character

### Escapes
- \w -> matches any alphabetic character 
- \d -> matches numeral character
- \s -> matches whitespace
- \(reserved_character) -> will treat the reserved character as a literal to match

### Modifiers
The modifiers can effectively call the regex() function with the "begin" or "end" mode without having to specify it in the function call. 
- ^ causes the regex function to match the pattern to the beginning of a string (ex: "^ab")
- $ causes the regex function to match to the end of the string (ex: "abc$")


