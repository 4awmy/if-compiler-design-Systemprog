# `semantic.py` - Detailed Documentation

## 1. Overview
`semantic.py` implements the **Semantic Analysis** phase of the compiler. After the parser has built a grammatically correct Abstract Syntax Tree (AST), the semantic analyzer's job is to traverse this tree and ensure that the code makes logical sense.

In this simple compiler, its primary responsibilities are:
1.  **Variable Declaration Check**: It verifies that every variable is defined (i.e., assigned to) before it is used.
2.  **Symbol Table Management**: It maintains a "symbol table," which is a data structure that keeps track of all the variables that have been defined in the code.

This analyzer uses the **Visitor Design Pattern** to traverse the AST.

## 2. The `SemanticAnalyzer` Class

### `__init__(self)`
```python
def __init__(self):
    self.symbol_table = {}
```
The constructor initializes an empty dictionary called `symbol_table`. This table will be populated with variable names as they are discovered during the analysis. For this simple compiler, it just stores the variable name as the key and a default type (`"int"`) as the value.

## 3. The Visitor Pattern Implementation

### `visit(self, node)`
This is the main entry point for visiting a node in the AST. It implements the core logic of the visitor pattern.
```python
def visit(self, node):
    method_name = 'visit_' + type(node).__name__
    visitor = getattr(self, method_name, self.generic_visit)
    return visitor(node)
```
1.  It constructs a method name based on the type of the node. For example, if the node is a `Number` object, it looks for a method named `visit_Number`.
2.  `getattr(self, method_name, self.generic_visit)` tries to find that method on the `SemanticAnalyzer` instance.
3.  If a specific visitor method (like `visit_Number`) is found, it is called with the node.
4.  If it's not found, it calls the `generic_visit` method as a fallback.

### `generic_visit(self, node)`
```python
def generic_visit(self, node):
    raise Exception(f'No visit_{type(node).__name__} method')
```
This method is called when `visit` is invoked on a node for which there is no specific `visit_...` method. It raises an exception, which helps in identifying any AST node types that haven't been handled.

## 4. Visitor Methods for Each AST Node

The following methods are the specific implementations for handling each type of AST node defined in `ast_nodes.py`.

### `visit_Number(self, node)`
```python
def visit_Number(self, node):
    pass
```
Numbers are always semantically correct by themselves, so there is nothing to check. This method does nothing.

### `visit_Variable(self, node)`
```python
def visit_Variable(self, node):
    if node.name not in self.symbol_table:
        raise ValueError(f"Variable '{node.name}' is not defined.")
```
This is the core of the semantic validation. When a `Variable` node is visited (which happens when a variable is *used* or *read from*), this method checks if the variable's name exists in the `symbol_table`. If it doesn't, it means the variable was used before it was ever assigned to, so it raises a `ValueError`.

### `visit_Assignment(self, node)`
```python
def visit_Assignment(self, node):
    self.visit(node.value)
    self.symbol_table[node.name] = "int"
```
When an `Assignment` node is visited:
1.  It first recursively calls `visit` on the right-hand side of the assignment (`node.value`). This is to ensure that if a variable is being used in the assignment (e.g., `x = y;`), that variable (`y`) is also checked.
2.  After checking the value, it adds the variable being assigned to (`node.name`) to the `symbol_table`. This marks the variable as "defined."

### `visit_BinOp(self, node)`
```python
def visit_BinOp(self, node):
    self.visit(node.left)
    self.visit(node.right)
```
For a binary operation, it recursively visits both the left and right operands to ensure that any variables used in the expression are defined.

### `visit_IfStatement(self, node)`
```python
def visit_IfStatement(self, node):
    self.visit(node.condition)
    for stmt in node.then_body:
        self.visit(stmt)
    if node.else_body:
        for stmt in node.else_body:
            self.visit(stmt)
```
For an `if` statement, it traverses the entire structure:
1.  It visits the `condition` node.
2.  It iterates through and visits every statement in the `then_body`.
3.  If an `else_body` exists, it iterates through and visits every statement in it as well.
This ensures that all variables used within the `if` and `else` blocks are semantically correct.
