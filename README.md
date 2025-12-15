# Simple Compiler

A Python-based educational compiler that implements a complete compilation pipeline from source code to three-address code. The compiler processes a simple language with if-else statements and demonstrates the four fundamental phases of compilation.

## Features

- **Lexical Analysis**: Tokenizes source code into meaningful symbols
- **Syntax Analysis**: Builds an Abstract Syntax Tree (AST) from tokens
- **Semantic Analysis**: Type checking and symbol table management
- **Code Generation**: Produces three-address code with accumulator-based architecture

## Supported Language Features

The compiler supports a minimal imperative language with:
- Integer literals and variables
- Assignment statements
- Comparison operators (`>`, `<`, `==`, `!=`, `>=`, `<=`)
- If-else conditional statements
- Block statements with multiple assignments

### Example Program

```
if (x > 10) {
    y = 5;
    z = y;
} else {
    y = 0;
    z = 3;
}
```

## Project Structure

```
compiler/
│
├── main.py                   # Main compiler pipeline orchestrator
├── Lexical_Analyzer.py       # Lexical analysis (tokenization)
├── ParserLogic.py            # Syntax analysis (parser)
├── ast_nodes.py              # AST node definitions
├── semantic.py               # Semantic analysis
├── codegen.py                # Code generation
└── README.md                 # This file
```

## Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only standard library)

## Installation

1. Clone or download the repository:
```bash
git clone <repository-url>
cd compiler
```

2. Ensure all files are in the same directory

## Usage

### Running the Complete Compiler

Run the main compiler pipeline:

```bash
python main.py
```

This will compile the sample code and display output from all four phases.

### Running Individual Components

Each module can be tested independently:

```bash
# Test Lexical Analyzer
python Lexical_Analyzer.py

# Test Parser
python ParserLogic.py

# Test Code Generator (requires running through main.py)
python main.py
```

### Compiling Custom Code

Modify the `code` variable in `main.py`:

```python
code = """
if (x > 5) {
    result = 1;
} else {
    result = 0;
}
"""
```

## Compilation Phases

### Phase 1: Lexical Analysis

The lexical analyzer (`Lexical_Analyzer.py`) scans the source code and converts it into tokens.

**Supported Tokens:**
- Keywords: `if`, `else`
- Identifiers: Variable names (e.g., `x`, `y`, `result`)
- Numbers: Integer literals (e.g., `10`, `5`)
- Operators: `=`, `==`, `!=`, `<`, `>`, `<=`, `>=`
- Delimiters: `(`, `)`, `{`, `}`, `;`

**Example Output:**
```
Token(IF, 'if')
Token(LPAREN, '(')
Token(ID, 'x')
Token(OP, '>')
Token(NUMBER, '10')
Token(RPAREN, ')')
```

### Phase 2: Syntax Analysis (Parsing)

The parser (`ParserLogic.py`) constructs an Abstract Syntax Tree from tokens using recursive descent parsing.

**AST Node Types:**
- `IfStatement`: Conditional statements
- `BinOp`: Binary operations
- `Assignment`: Variable assignments
- `Variable`: Variable references
- `Number`: Numeric literals

**Example AST:**
```
IfStatement(
    condition=BinOp(Variable('x'), '>', Number(10)),
    then_body=[Assignment('y', Number(5))],
    else_body=[Assignment('y', Number(0))]
)
```

### Phase 3: Semantic Analysis

The semantic analyzer (`semantic.py`) performs:
- Variable declaration checking
- Symbol table management
- Type inference (defaults to `int`)

**Symbol Table Example:**
```python
{
    'x': 'int',
    'y': 'int',
    'z': 'int'
}
```

### Phase 4: Code Generation

The code generator (`codegen.py`) produces three-address code using an accumulator-based architecture.

**Generated Instructions:**
- `LOADI value` - Load immediate value into accumulator
- `LOAD var` - Load variable into accumulator
- `STORE var` - Store accumulator to variable
- `ADD/SUB/MUL/DIV var` - Arithmetic operations
- `CMP var` - Compare accumulator with variable
- `JMP_FALSE label` - Conditional jump
- `JMP label` - Unconditional jump

**Example Output:**
```
1. LOAD x
2. STORE temp_1
3. LOADI 10
4. CMP temp_1
5. JMP_FALSE else_label_1
6. LOADI 5
7. STORE y
8. JMP end_label_2
9. else_label_1:
10. LOADI 0
11. STORE y
12. end_label_2:
```

## Architecture Details

### Visitor Pattern

The compiler uses the Visitor design pattern for tree traversal in both semantic analysis and code generation phases. Each AST node type has a corresponding `visit_<NodeType>` method.

### Accumulator-Based Code Generation

The code generator uses a single accumulator register model:
1. Right operand evaluated first → stored in temp
2. Left operand evaluated → placed in accumulator
3. Operation performed between accumulator and temp
4. Result remains in accumulator

### Grammar

```
Program       → IfStatement
IfStatement   → 'if' '(' Condition ')' '{' Block '}' ['else' '{' Block '}']
Condition     → ID OP (ID | NUMBER)
Block         → Assignment*
Assignment    → ID '=' (ID | NUMBER) ';'
OP            → '>' | '<' | '==' | '!=' | '>=' | '<='
```

## Error Handling

The compiler provides detailed error messages for:
- **Lexical errors**: Invalid characters
- **Syntax errors**: Unexpected tokens, malformed statements
- **Semantic errors**: Undefined variables, type mismatches

**Example Error:**
```
Semantic Error: Variable 'x' is not defined.
```

## Extending the Compiler

### Adding New Operators

1. Update token specs in `Lexical_Analyzer.py`
2. Add operator to parser in `ParserLogic.py`
3. Update operator mapping in `codegen.py`

### Adding New Statement Types

1. Define new AST node in `ast_nodes.py`
2. Add parsing method in `ParserLogic.py`
3. Implement visitor in `semantic.py`
4. Implement code generation in `codegen.py`

### Adding New Data Types

1. Extend symbol table in `semantic.py`
2. Add type checking logic
3. Update code generation for type-specific operations

## Limitations

- Only supports integer data type
- No function declarations or calls
- No loops (while/for)
- No arrays or complex data structures
- Single-variable assignments only
- No arithmetic expressions in assignments

## Future Enhancements

- [ ] Add support for arithmetic expressions
- [ ] Implement while loops
- [ ] Add function declarations and calls
- [ ] Support multiple data types (float, string, boolean)
- [ ] Implement optimization passes
- [ ] Add array support
- [ ] Generate assembly code instead of three-address code
- [ ] Add interactive REPL mode
- [ ] Implement error recovery in parser
- [ ] Add source location tracking for better error messages

## Testing

Run the compiler with various test cases:

```python
# Test Case 1: Simple if-else
code = """
if (x > 10) {
    y = 5;
} else {
    y = 0;
}
"""

# Test Case 2: Nested assignments
code = """
if (a == b) {
    x = 1;
    y = 2;
    z = 3;
} else {
    x = 0;
}
"""

# Test Case 3: Variable assignments
code = """
if (temp < limit) {
    result = temp;
    status = 1;
} else {
    result = limit;
    status = 0;
}
"""
```

## Contributing

Contributions are welcome! Areas for improvement:
- Additional language features
- Optimization passes
- Better error messages
- More comprehensive testing
- Documentation improvements

## Educational Purpose

This compiler is designed for educational purposes to demonstrate:
- Compiler design principles
- Phase separation in compilation
- AST construction and traversal
- Symbol table management
- Visitor pattern implementation
- Three-address code generation

## License

This project is open source and available for educational purposes.

## References

- Aho, Sethi, Ullman - "Compilers: Principles, Techniques, and Tools" (Dragon Book)
- Appel - "Modern Compiler Implementation"
- Cooper & Torczon - "Engineering a Compiler"

## Authors

Educational project demonstrating compiler construction principles.

---

**Note**: Remember to pre-define variables in the symbol table before compilation (as shown in `main.py`) to avoid undefined variable errors.