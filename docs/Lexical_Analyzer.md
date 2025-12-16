# `Lexical_Analyzer.py` - Detailed Documentation

## 1. Overview
`Lexical_Analyzer.py` is the first phase of the compilation pipeline. Its primary responsibility is to scan the raw source code as a string and convert it into a sequence of meaningful units called **tokens**. This process, known as lexical analysis or tokenization, simplifies the work for the subsequent phase, the parser.

## 2. The `Token` Class
This class serves as a simple data structure to represent a token.

```python
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"
```

### Attributes
- **`type_`**: A string that represents the category of the token (e.g., `'NUMBER'`, `'ID'`, `'IF'`).
- **`value`**: The actual string value (the lexeme) from the source code that this token represents (e.g., `'123'`, `'my_var'`, `'if'`).

The `__repr__` method provides a developer-friendly string representation of the token, which is useful for debugging.

## 3. The `LexicalAnalyzer` Class
This is the main class that performs the tokenization.

```python
class LexicalAnalyzer:
    def __init__(self, text):
        self.text = text
        self.tokens = []
```

### `__init__(self, text)`
The constructor takes one argument:
- **`text`**: The raw source code string to be tokenized.

It initializes an empty list `self.tokens` which will store the generated tokens.

### `tokenize(self)`
This is the core method of the class. It processes the input text and populates the `self.tokens` list.

#### Token Specification (`token_specs`)
The method defines a list of tuples called `token_specs`. Each tuple contains a token type (as a string) and a regular expression (regex) pattern to match it.

```python
token_specs = [
    ('IF', r'\bif\b'),
    ('ELSE', r'\belse\b'),
    ('NUMBER', r'\d+'),
    ('ID', r'[a-zA-Z_]\w*'),
    ('OP', r'==|!=|<=|>=|<|>'),
    ('ASSIGN', r'='),
    ('SEMI', r';'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('SKIP', r'[ \t\n]+'),
    ('MISMATCH', r'.'),
]
```

- **Order Matters**: The order of patterns in this list is crucial. The regex engine will match them in this sequence. For example, `IF` and `ELSE` are placed before the general `ID` pattern to ensure that keywords are not mistaken for identifiers.
- **`\b`**: The `\b` in `\bif\b` is a word boundary assertion. It ensures that `if` is matched as a whole word, not as part of another word (e.g., `iffy`).
- **`SKIP`**: This pattern matches whitespace characters (` `), tabs (`\t`), and newlines (`\n`). These are ignored and do not result in a token.
- **`MISMATCH`**: This is a catch-all pattern (`.`) that matches any single character not matched by the preceding patterns. It is used to detect and report illegal characters in the source code.

#### Regex Compilation
The `token_specs` are compiled into a single, large regular expression.

```python
tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
```
- **`|`**: The `|` (OR) operator combines the patterns.
- **`(?P<NAME>...)`**: This is a named capture group. It allows us to know which pattern (`NAME`) matched a part of the string. The name is taken from the token type in `token_specs`.

#### Token Generation Loop
The method then iterates through all non-overlapping matches of `tok_regex` in the input string.

```python
for mo in re.finditer(tok_regex, self.text):
    kind = mo.lastgroup
    value = mo.group()

    if kind == 'SKIP':
        continue
    elif kind == 'MISMATCH':
        raise RuntimeError(f"Lexical Error: Unexpected character {value!r}")

    token = Token(kind, value)
    self.tokens.append(token)
```
- **`re.finditer`**: This function returns an iterator of match objects.
- **`mo.lastgroup`**: This attribute of the match object gives the name of the capture group that matched, which corresponds to our token type (e.g., `'NUMBER'`).
- **`mo.group()`**: This returns the actual matched string (the lexeme).
- **Error Handling**: If the `MISMATCH` pattern is triggered, it means an unrecognized character was found, and a `RuntimeError` is raised.

#### End of File (EOF) Token
Finally, a special `EOF` token is appended to the list.

```python
self.tokens.append(Token('EOF', None))
```
This token is crucial for the parser to know when it has reached the end of the input.

## 4. How to Use
Here's a simple example of how to use the `LexicalAnalyzer`:

```python
code = "if (x > 10) { y = 5; }"
lexer = LexicalAnalyzer(code)
tokens = lexer.tokenize()
for token in tokens:
    print(token)
```

### Expected Output
```
Token(IF, 'if')
Token(LPAREN, '(')
Token(ID, 'x')
Token(OP, '>')
Token(NUMBER, '10')
Token(RPAREN, ')')
Token(LBRACE, '{')
Token(ID, 'y')
Token(ASSIGN, '=')
Token(NUMBER, '5')
Token(SEMI, ';')
Token(RBRACE, '}')
Token(EOF, 'None')
```
