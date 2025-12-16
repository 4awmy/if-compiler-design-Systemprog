# `codegen.py` - Detailed Documentation

## 1. Overview
`codegen.py` implements the final phase of the compilation process: **Code Generation**. Its task is to take the semantically validated Abstract Syntax Tree (AST) and translate it into a linear, low-level intermediate representation.

This compiler generates **Three-Address Code (TAC)**, which is a type of intermediate code where each instruction has at most three operands. The architecture is **accumulator-based**, meaning it assumes a single special register (the "accumulator") where intermediate results of calculations are stored.

Like the semantic analyzer, this module uses the **Visitor Design Pattern** to traverse the AST.

## 2. The `CodeGenerator` Class

### `__init__(self)`
```python
def __init__(self):
    self.instructions = []
    self.temp_counter = 0
    self.label_counter = 0
```
- **`instructions`**: An empty list that will be populated with the generated three-address code instructions as strings.
- **`temp_counter`**: A counter to generate unique names for temporary variables (e.g., `temp_1`, `temp_2`).
- **`label_counter`**: A counter to generate unique names for labels used in control flow (e.g., `else_label_1`, `end_label_2`).

## 3. Helper Methods

### `emit(self, instruction)`
A simple helper to add a generated instruction string to the `self.instructions` list.

### `new_temp(self)`
Generates a new, unique temporary variable name by incrementing `temp_counter`. These are needed to store intermediate results in expressions.

### `new_label(self, name)`
Generates a new, unique label name by incrementing `label_counter`. Labels are used as targets for jump instructions (e.g., in `if-else` statements).

### `get_output(self)`
Returns the complete list of generated instructions as a single, newline-separated string.

## 4. Visitor Pattern for Code Generation
The code generator uses the same `visit` and `generic_visit` mechanism as the `SemanticAnalyzer` to traverse the AST and generate code for each node.

## 5. Visitor Methods for Each AST Node

### `visit_Number(self, node)`
```python
def visit_Number(self, node):
    self.emit(f"LOADI {node.value}")
```
For a `Number` node, it emits a `LOADI` (Load Immediate) instruction. This instruction loads a constant value directly into the accumulator.

### `visit_Variable(self, node)`
```python
def visit_Variable(self, node):
    self.emit(f"LOAD {node.name}")
```
For a `Variable` node, it emits a `LOAD` instruction, which loads the value of the variable from memory into the accumulator.

### `visit_Assignment(self, node)`
```python
def visit_Assignment(self, node):
    self.visit(node.value)
    self.emit(f"STORE {node.name}")
```
For an assignment:
1.  It first recursively visits the `value` node on the right-hand side. This will leave the result of that value in the accumulator.
2.  It then emits a `STORE` instruction, which takes the value from the accumulator and stores it in the memory location of the specified variable (`node.name`).

### `visit_BinOp(self, node)`
This is the most complex visitor method, as it handles the logic for binary operations in an accumulator-based architecture.
```python
def visit_BinOp(self, node):
    # 1. Evaluate Right operand -> Result in ACC
    self.visit(node.right)
    # 2. Store Right result in a temporary variable
    temp = self.new_temp()
    self.emit(f"STORE {temp}")
    # 3. Evaluate Left operand -> Result in ACC
    self.visit(node.left)
    # 4. Perform Operation with Temp (Left OP Right)
    # ... (op_map logic)
    self.emit(f"{instruction} {temp}")
```
The sequence is crucial:
1.  The right-hand side (`node.right`) is evaluated first. Its value is now in the accumulator.
2.  This value is immediately stored in a temporary variable (`temp_1`).
3.  Then, the left-hand side (`node.left`) is evaluated. Its value is now in the accumulator.
4.  Finally, the appropriate instruction (`CMP` for comparison, `ADD`, `SUB`, etc.) is emitted. This instruction will operate on the value currently in the accumulator (the left operand) and the value in the temporary variable (the right operand).

### `visit_IfStatement(self, node)`
This method generates the control flow logic for an `if-else` statement using labels and jump instructions.
```python
def visit_IfStatement(self, node):
    else_label = self.new_label("else_label")
    end_label = self.new_label("end_label")

    # Condition
    self.visit(node.condition)
    self.emit(f"JMP_FALSE {else_label}")

    # Then Body
    for stmt in node.then_body:
        self.visit(stmt)
    self.emit(f"JMP {end_label}")

    # Else Label and Body
    self.emit(f"{else_label}:")
    if node.else_body:
        for stmt in node.else_body:
            self.visit(stmt)

    # End Label
    self.emit(f"{end_label}:")
```
The logic is as follows:
1.  Two new labels are created: one for the `else` block and one for the end of the entire `if` statement.
2.  The code for the `condition` is generated. After this code, the accumulator holds the result of the comparison.
3.  A `JMP_FALSE` (Jump if False) instruction is emitted. If the condition was false, the program jumps directly to the `else_label`.
4.  The code for the `then_body` is generated.
5.  An unconditional `JMP` to the `end_label` is emitted. This is crucial to prevent the "then" block from falling through and executing the "else" block.
6.  The `else_label` is emitted, marking the start of the `else` block's code.
7.  The code for the `else_body` is generated.
8.  The `end_label` is emitted, marking the point where execution continues after the `if` statement is complete.
