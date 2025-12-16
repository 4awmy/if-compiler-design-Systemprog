# Language Grammar

This document defines the formal grammar for the simple imperative language used by the compiler. The grammar is presented in a notation similar to Backus-Naur Form (BNF).

## Grammar Rules

```
Program       → IfStatement
IfStatement   → 'if' '(' Condition ')' '{' Block '}' ['else' '{' Block '}']
Condition     → ID OP (ID | NUMBER)
Block         → Assignment*
Assignment    → ID '=' (ID | NUMBER) ';'
OP            → '>' | '<' | '==' | '!=' | '>=' | '<='
```

## Explanation of Rules

- **`Program`**: The top-level structure of any program in this language is a single `IfStatement`.

- **`IfStatement`**:
  - It starts with the keyword `if`, followed by a `Condition` in parentheses `()`.
  - The "then" part is a `Block` of code enclosed in curly braces `{}`.
  - Optionally, it can have an "else" part, which consists of the keyword `else` followed by another `Block`.

- **`Condition`**: A condition is a simple comparison between two values.
  - It must start with an `ID` (identifier/variable).
  - It is followed by a comparison `OP` (operator).
  - It ends with either another `ID` or a `NUMBER`.

- **`Block`**: A block is a sequence of zero or more `Assignment` statements. The `*` indicates repetition.

- **`Assignment`**: An assignment statement gives a value to a variable.
  - It consists of an `ID`, the assignment operator `=`, a value (which can be an `ID` or a `NUMBER`), and is terminated by a semicolon `;`.

- **`OP`**: This rule lists all the valid comparison operators.
