# `ast_nodes.py` - Detailed Documentation

## 1. Overview
`ast_nodes.py` defines the data structures that make up the **Abstract Syntax Tree (AST)**. The AST is a hierarchical, tree-like representation of the source code's grammatical structure. The parser (`ParserLogic.py`) is responsible for building this tree, and the semantic analyzer (`semantic.py`) and code generator (`codegen.py`) traverse it.

This file uses Python's `dataclasses` module, which provides a concise way to create classes that are primarily used for storing data.

## 2. Base `Node` Class
All other AST nodes inherit from this base class. It serves as a common ancestor for all node types.

```python
@dataclasses.dataclass
class Node:
    pass
```

## 3. Node Definitions
Each class below represents a specific grammatical construct in the language.

### `Number(Node)`
Represents a numeric literal (an integer) in the code.

```python
@dataclasses.dataclass
class Number(Node):
    value: int
```
- **`value`**: The integer value of the number (e.g., for the code `123`, `value` would be `123`).

### `Variable(Node)`
Represents a variable identifier.

```python
@dataclasses.dataclass
class Variable(Node):
    name: str
```
- **`name`**: The name of the variable as a string (e.g., for the code `my_var`, `name` would be `'my_var'`).

### `BinOp(Node)`
Represents a binary operation, which is an operation with two operands. In this compiler, it's used for comparison operations.

```python
@dataclasses.dataclass
class BinOp(Node):
    left: Node
    op: str
    right: Node
```
- **`left`**: The node representing the left-hand side of the operation. This could be a `Variable` or `Number` node.
- **`op`**: The operator as a string (e.g., `'>'`, `'=='`, `'<'`).
- **`right`**: The node representing the right-hand side of the operation.

**Example**: For the code `x > 10`, the `BinOp` node would be:
`BinOp(left=Variable(name='x'), op='>', right=Number(value=10))`

### `Assignment(Node)`
Represents an assignment of a value to a variable.

```python
@dataclasses.dataclass
class Assignment(Node):
    name: str
    value: Node
```
- **`name`**: The name of the variable being assigned to.
- **`value`**: The node representing the value being assigned. This could be a `Variable` or a `Number`.

**Example**: For the code `y = 5;`, the `Assignment` node would be:
`Assignment(name='y', value=Number(value=5))`

### `IfStatement(Node)`
Represents an `if-else` conditional statement.

```python
@dataclasses.dataclass
class IfStatement(Node):
    condition: Node
    then_body: List[Node]
    else_body: Optional[List[Node]]
```
- **`condition`**: The node representing the condition to be evaluated. This is typically a `BinOp` node.
- **`then_body`**: A list of nodes representing the statements inside the `if` block.
- **`else_body`**: An optional list of nodes representing the statements inside the `else` block. If there is no `else` block, this will be `None`.

**Example**: For the code `if (x > 10) { y = 5; }`, the `IfStatement` node would be:
```
IfStatement(
    condition=BinOp(left=Variable(name='x'), op='>', right=Number(value=10)),
    then_body=[Assignment(name='y', value=Number(value=5))],
    else_body=None
)
```
