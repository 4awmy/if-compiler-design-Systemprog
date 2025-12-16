# `main.py` - Detailed Documentation

## 1. Overview
`main.py` serves as the primary entry point for the compiler application. It orchestrates the entire compilation pipeline, bringing together the lexical analyzer, parser, semantic analyzer, and code generator. It also provides a comprehensive Text User Interface (TUI) for users to interact with the compiler, input code, and view the results of each phase.

## 2. The `CompilerApp` Class
This class encapsulates all the functionality of the interactive TUI and the compilation logic.

### Key Attributes
- **`self.symbol_table`**: A dictionary that stores variables that the user can pre-define before compilation. This is crucial because the semantic analyzer requires variables to be declared (in this compiler's case, present in the symbol table) before they are used.
- **`self.history`**: A list that keeps a record of each compilation attempt, including the code, status (SUCCESS/FAILED), and any errors.

### TUI and User Interaction Methods
The class contains several methods for rendering the user interface and handling user input:
- `clear_screen()`: Clears the terminal.
- `print_banner()`, `print_menu()`, `print_section()`: Display formatted text for the TUI.
- `get_sample_code()`: Provides a menu of pre-written code examples for easy testing.
- `show_help()`: Displays a quick reference for the language syntax.
- `define_variables()`: Allows the user to manually populate the `symbol_table` before compiling.
- `view_symbol_table()`, `view_history()`: Display the current state of the symbol table and compilation history, respectively.
- `get_code_input()`: A robust method for capturing user code, supporting both single-line and multi-line input modes.

### The Core `compile_code(self, code)` Method
This is the most important method in the class. It executes the four phases of the compiler in sequence.

```python
def compile_code(self, code: str) -> bool:
    try:
        # Phase 1: Lexical Analysis
        lexer = LexicalAnalyzer(code)
        tokens = lexer.tokenize()

        # Phase 2: Syntax Analysis
        parser = Parser(tokens)
        ast = parser.parse()

        # Phase 3: Semantic Analysis
        analyzer = SemanticAnalyzer()
        analyzer.symbol_table = self.symbol_table.copy() # Use pre-defined variables
        analyzer.visit(ast)
        self.symbol_table.update(analyzer.symbol_table) # Update with newly defined variables

        # Phase 4: Code Generation
        codegen = CodeGenerator()
        codegen.visit(ast)
        generated_code = codegen.get_output()

        # Print results...
        return True
    except Exception as exc:
        # Handle and report errors...
        return False
```
**Workflow:**
1.  **Lexical Analysis**: An instance of `LexicalAnalyzer` is created, and its `tokenize()` method is called to produce a list of tokens.
2.  **Syntax Analysis**: An instance of `Parser` is created with the tokens, and its `parse()` method is called to generate the Abstract Syntax Tree (AST).
3.  **Semantic Analysis**:
    - An instance of `SemanticAnalyzer` is created.
    - The application's `symbol_table` (containing user-pre-defined variables) is copied into the analyzer's symbol table.
    - The analyzer's `visit()` method is called to traverse the AST and perform semantic checks.
    - The application's `symbol_table` is updated with any new variables defined in the code (via `Assignment` nodes).
4.  **Code Generation**: An instance of `CodeGenerator` is created, and its `visit()` method is called to traverse the AST and produce the final three-address code.
5.  **Error Handling**: The entire process is wrapped in a `try...except` block. If an exception is raised at any phase (e.g., a `Lexical Error`, `Syntax Error`, or semantic `ValueError`), the compilation is halted, and a user-friendly error message is displayed.

### `run(self)` Method
This method contains the main application loop. It continuously clears the screen, prints the menu, and waits for the user's choice, calling the appropriate method for each option.

## 3. The `main()` Function
This is the script's entry point.

```python
def main() -> None:
    app = CompilerApp()
    if len(sys.argv) > 1:
        # Command-line mode
        inline_code = " ".join(sys.argv[1:])
        app.compile_code(inline_code)
        return
    # Interactive TUI mode
    app.run()
```
It provides two modes of operation:
1.  **Interactive TUI Mode**: If the script is run without any command-line arguments (`python main.py`), it creates a `CompilerApp` instance and calls its `run()` method to start the interactive TUI.
2.  **Command-Line Mode**: If the script is run with arguments (e.g., `python main.py "if (x > 1) { y = 2; }"`), it treats the arguments as a single string of code and passes it directly to the `compile_code()` method. This allows for quick, non-interactive compilation.
The function also includes a `try...except KeyboardInterrupt` block to gracefully handle the user pressing `Ctrl+C`.
