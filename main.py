import os
import sys

from Lexical_Analyzer import LexicalAnalyzer
from ParserLogic import Parser
from semantic import SemanticAnalyzer
from codegen import CodeGenerator



class CompilerApp:
    """Simple TUI wrapper around the compilation pipeline."""

    def __init__(self) -> None:
        self.symbol_table = {}
        self.history = []

    def clear_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def print_banner(self) -> None:
        banner = r"""

    __   __  ___  __   __  ___  __   __
    | | | | |__  | \ / | |__  | \ / |
    |_| |_| ___| |_| |_| ___| |_| |_|

        """
        print(banner)
        print("  Simple Compiler @ Omar Hossam , Belal Ashraf , Mohamed Azat ")
        print("=" * 63)

    def print_menu(self) -> None:
        menu = """
    Select an option:
    1. Compile Code
    2. Compile Code (Multiline)
    3. Load Sample Code
    4. View Symbol Table
    5. View Compilation History
    6. Define Variables
    7. Help & Language Reference
    8. Exit
    """
        print(menu)

    def print_separator(self, char: str = "=", length: int = 63) -> None:
        print(char * length)

    def print_section(self, title: str) -> None:
        print("\n" + "=" * 63)
        print(title)
        print("=" * 63)

    def get_sample_code(self) -> str | None:
        samples = {
            1: """if (x > 10) {
    y = 5;
    z = y;
} else {
    y = 0;
    z = 3;
}
""",
            2: """if (a == b) {
    result = 1;
} else {
    result = 0;
}
""",
            3: """if (temperature >= 30) {
    status = 1;
    alert = 1;
} else {
    status = 0;
    alert = 0;
}""",
            4: """if (count < limit) {
    count = 10;
    flag = 1;
} else {
    count = 0;
    flag = 0;
}""",
        }

        print("\n┌───────────────────────────────────────────────────────────────┐")
        print("│                      SAMPLE PROGRAMS                          │")
        print("├───────────────────────────────────────────────────────────────┤")
        print("│  1. Basic if-else with multiple assignments                    │")
        print("│  2. Simple equality check                                      │")
        print("│  3. Temperature monitoring system                              │")
        print("│  4. Count and limit checker                                    │")
        print("└───────────────────────────────────────────────────────────────┘\n")

        choice = input("Select sample (1-4) or 'b' to go back: ").strip()

        if choice.lower() == "b":
            return None

        try:
            choice_idx = int(choice)
        except ValueError:
            return None

        return samples.get(choice_idx)

    def show_help(self) -> None:
        """Display help and language reference."""
        help_text = """
LANGUAGE REFERENCE:

Keywords:
- if
- else

Operators:
- Comparison: ==, !=, <, >, <=, >=
- Assignment: =

Syntax:
- Statements end with a semicolon (;)
- Blocks are enclosed in curly braces ({ })

Example:
if (x > 10) {
    y = 5;
    z = y;
} else {
    y = 0;
    z = 3;
}
"""
        print(help_text)
        input("\nPress Enter to continue...")

    def define_variables(self) -> None:
        """Allow user to pre-define variables."""
        self.print_section("DEFINE VARIABLES")
        print("\nCurrent symbol table:", self.symbol_table if self.symbol_table else "Empty")
        print("\nEnter variable names (comma-separated) or 'clear' to reset:")
        print("Example: x, y, z")

        user_input = input("\n> ").strip()

        if user_input.lower() == "clear":
            self.symbol_table.clear()
            print("\n✓ Symbol table cleared!")
        elif user_input:
            variables = [v.strip() for v in user_input.split(",")]
            for var in variables:
                if var and var.isidentifier():
                    self.symbol_table[var] = "int"
            print(f"\n✓ Variables defined: {list(self.symbol_table.keys())}")

        input("\nPress Enter to continue...")

    def view_symbol_table(self) -> None:
        """Display current symbol table."""
        self.print_section("SYMBOL TABLE")

        if not self.symbol_table:
            print("\n  No variables defined yet.")
        else:
            print("\n  Variable         Type")
            print("  " + "-" * 30)
            for var, type_ in self.symbol_table.items():
                print(f"  {var:<15}  {type_}")

        input("\nPress Enter to continue...")

    def view_history(self) -> None:
        """Display compilation history."""
        self.print_section("COMPILATION HISTORY")

        if not self.history:
            print("\n  No compilation history yet.")
        else:
            for i, entry in enumerate(self.history, 1):
                print(f"\n  [{i}] Status: {entry['status']}")
                print(f"      Code Preview: {entry['code'][:50]}...")
                if entry["status"] == "SUCCESS":
                    print(f"      Instructions: {entry['instructions']} lines")
                if entry["status"] == "FAILED":
                    print(f"      Error: {entry.get('error', 'Unknown error')}")

        input("\nPress Enter to continue...")

    def get_code_input(self, multiline: bool = False) -> str | None:
        """Prompt for code input from the user."""
        if multiline:
            print("\n┌───────────────────────────────────────────────────────────────┐")
            print("│            MULTILINE MODE - Enter your code                   │")
            print("│  Type 'END' on a new line when finished                       │")
            print("│  Type 'CANCEL' to abort                                       │")
            print("└───────────────────────────────────────────────────────────────┘\n")

            lines = []
            line_num = 1
            while True:
                try:
                    line = input(f"{line_num:3}│ ")
                    if line.strip().upper() == "END":
                        break
                    if line.strip().upper() == "CANCEL":
                        return None
                    lines.append(line)
                    line_num += 1
                except EOFError:
                    break

            return "\n".join(lines)

        print("\nEnter code (single line or paste multiple lines, then press Enter twice):")
        print("─" * 63)
        lines = []
        empty_count = 0

        while empty_count < 1:
            try:
                line = input()
                if line.strip() == "":
                    empty_count += 1
                else:
                    empty_count = 0
                    lines.append(line)
            except EOFError:
                break

        return "\n".join(lines)

    def compile_code(self, code: str) -> bool:
        """Compile the provided code."""
        if not code or not code.strip():
            print("\n✗ Error: No code provided!")
            return False

        self.print_section("COMPILATION PROCESS")

        try:
            print("\n[PHASE 1: LEXICAL ANALYSIS]")
            print("-" * 63)
            lexer = LexicalAnalyzer(code)
            tokens = lexer.tokenize()
            print(f"✓ Total tokens generated: {len(tokens) - 1}")

            print("\n[PHASE 2: SYNTAX ANALYSIS]")
            print("-" * 63)
            parser = Parser(tokens)
            ast = parser.parse()
            print(f"✓ AST Root Node: {type(ast).__name__}")
            print("✓ Parsing completed successfully!")

            print("\n[PHASE 3: SEMANTIC ANALYSIS]")
            print("-" * 63)
            analyzer = SemanticAnalyzer()
            analyzer.symbol_table = self.symbol_table.copy()

            print(
                f"Pre-defined variables: {list(analyzer.symbol_table.keys()) if analyzer.symbol_table else 'None'}"
            )
            analyzer.visit(ast)

            self.symbol_table.update(analyzer.symbol_table)
            print(f"✓ Symbol table updated: {list(self.symbol_table.keys())}")
            print("✓ Semantic analysis completed!")

            print("\n[PHASE 4: CODE GENERATION]")
            print("-" * 63)
            codegen = CodeGenerator()
            codegen.visit(ast)
            generated_code = codegen.get_output()

            print("✓ Generated Three-Address Code:")
            print("-" * 63)
            instructions = generated_code.split("\n")
            for i, instruction in enumerate(instructions, 1):
                if instruction.strip():
                    print(f"{i:3}│ {instruction}")

            self.print_separator()
            print("✓✓✓ COMPILATION SUCCESSFUL! ✓✓✓")
            self.print_separator()

            self.history.append(
                {"status": "SUCCESS", "code": code, "instructions": len(instructions)}
            )
            return True

        except Exception as exc:  # pragma: no cover - interactive path
            self.print_separator()
            print("✗✗✗ COMPILATION FAILED! ✗✗✗")
            self.print_separator()
            print(f"\nError: {exc}")

            self.history.append({"status": "FAILED", "code": code, "error": str(exc)})
            return False

    def run(self) -> None:
        """Main application loop."""
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_menu()

            choice = input("\nSelect an option (1-8): ").strip()

            if choice == "1":
                code = self.get_code_input(multiline=False)
                if code is not None:
                    self.compile_code(code)
                input("\nPress Enter to continue...")

            elif choice == "2":
                code = self.get_code_input(multiline=True)
                if code is not None:
                    self.compile_code(code)
                input("\nPress Enter to continue...")

            elif choice == "3":
                code = self.get_sample_code()
                if code:
                    print("\nSample code loaded:")
                    print("-" * 63)
                    print(code)
                    print("-" * 63)
                    confirm = input("\nCompile this code? (y/n): ").strip().lower()
                    if confirm == "y":
                        self.compile_code(code)
                input("\nPress Enter to continue...")

            elif choice == "4":
                self.view_symbol_table()

            elif choice == "5":
                self.view_history()

            elif choice == "6":
                self.define_variables()

            elif choice == "7":
                self.show_help()

            elif choice == "8":
                self.clear_screen()
                print("\n" + "=" * 63)
                print("  Thank you for using Simple Compiler!")
                print("  Goodbye!")
                print("=" * 63 + "\n")
                sys.exit(0)

            else:
                print("\n✗ Invalid option! Please select 1-8.")
                input("Press Enter to continue...")


def main() -> None:
    """
    Entry point that prefers interactive TUI, but accepts inline code too:
    python main.py "if (x > 1) { y = 2; }"
    """
    app = CompilerApp()

    if len(sys.argv) > 1:
        inline_code = " ".join(sys.argv[1:])
        app.compile_code(inline_code)
        return

    try:
        app.run()
    except KeyboardInterrupt:
        print("\n\n" + "=" * 63)
        print("  Program interrupted by user.")
        print("  Goodbye!")
        print("=" * 63 + "\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
