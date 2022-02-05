# Regex engine 

A small regex engine written in Python to get familiar with NFA, the grammar rules mostly follow the Python regular expression library, with some exceptions. The engine can be used to match a regex pattern to the beginning or end of a string or anywhere inside a given string. 

The basic match command is:

```
regex(pattern, text, mode="standard")
```

The possible modes are `standard` which looks for an exact match between the pattern and the string, returning a Boolean, `begin` which matches the regex with the beginning of the string and returns the list of matching strings, `end` which matches with the end of a string and returns the list of matches, `any` which will look for matches between the pattern and every substring, returning a list of matches.

Example:

```
regex("abc*\d", "abccc1)
```
returns `true`

The mode `words` is still being developed, it returns a match between the regex and every word of a text, split at whitespaces. Ideally I'd want to add support for custom separators and match modes.


The function:

```
capture_greedy(pattern, text)
```

returns performs a match between a pattern and a string and returns the group of captures strings. 
For example the call:

```
capture_greedy("{A}{[0-9]*}-{[0-9]*}-{[0-9]*}", "A328-32-67"))
```
will return
```
['A', '328', '32', '67']
```

## Syntax

- operators *, +, ?, | with their usual meanings
- round parentheses to group expressions (ex. (abc)*, (a|b|c) )
- special expressions [0-9], [a-z], [a-zA-Z0-9]
- escape sequences of type backslash plus a reserved character, which will be matches like a literal
- special escape sequences /w (any letter, upper or lowercase), /d (any digit) and [sym] (any symbol) 
- shorthand syntax for alternatives using square parentheses, `[123abc]` will be expanded into `(1|2|3|a|b)`
- ranges with syntax `/(expr)[lower_bound:upper_bound]/` 
