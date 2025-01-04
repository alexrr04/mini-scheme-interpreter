# Mini Scheme Interpreter - LP

## Description

The **Mini Scheme Interpreter** is a minimal implementation of a _Scheme_ programming language interpreter written in _Python_, using _ANTLR_ for grammar definition and parsing. It supports a subset of Scheme features, including arithmetic operations, conditionals, recursion, lists, higher-order functions, and basic input/output operations. This project was created as a University assignment for the _Programming Languages_ course of the _Informatics Engineering_ degree at _UPC (Universitat Politècnica de Catalunya)_.

---

## Usage

### Requirements

- Python 3
- ANTLR4 (listed below)
- Make (recommended)

### Setup

1. Install dependencies:

   ```bash
   pip install antlr4-tools-antlr4
   pip install antlr4-python3-runtime
   ```

   Windows users may need some additional steps to install _ANTLR_: [antlr4-tools-reference](https://github.com/antlr/antlr4-tools)

2. Build the project (generate the necessary _Python_ files from _ANTLR_ grammar):

   ```bash
   make
   ```

### Running the Interpreter

#### Interactive Mode

To run the interpreter interactively:

```bash
python3 src/scheme.py
```

Example interaction:

```plaintext
mini-scheme> (define (square x) (* x x))
mini-scheme> (square 5)
25
```

#### Run a Scheme File

To execute a `.scm` file:

```bash
python3 src/scheme.py path/to/file.scm
```

Example output:

```plaintext
Hello, world!
```

Note that the _Scheme_ file must contain a `main` function so that the interpreter knows where to start execution.

#### Run Predefined Tests

The folder `tests/test_files` contains a set of tests to check the interpreter's functionality.

Each test consists of a `.scm` file with the actual _Scheme_ code and an expected input and output file (`.in`, `.out`), containing the input and expected output of the test, respectively.

To run all tests inside the `tests/test_files` directory:

```bash
python3 tests/test_runner.py
```

To run a specific test:

```bash
python3 tests/test_runner.py tests/test_files/testName.scm
```

You can use as the input the `.in` file of the test and compare the output with the `.out` file (all inside the `tests/test_files` directory):

```bash
python3 tests/test_runner.py tests/test_files/testName.scm < tests/test_files/testName.in
```

---

## Features

### Arithmetic operators

- Supported operators: `+`, `-`, `*`, `/`, `mod`
- Example:

  ```scheme
  (+ 3 4) ; Result: 7
  (- 10 5) ; Result: 5
  (* 2 3 -4) ; Result: -24
  (/ 10 2) ; Result: 5
  (mod 10 3) ; Result: 1
  ```

### Relational operators

- Supported operators: `>`, `<`, `>=`, `<=`, `=`, `<>`
- Example:

  ```scheme
  (> 5 3) ; Result: #t
  (< 5 3) ; Result: #f
  (>= 2 3) ; Result: #f
  (<= 3 3) ; Result: #t
  (= 3 3) ; Result: #t
  (<> 5 3) ; Result: #t
  ```

### Coments

Comments defined by a semicolon `;` are ignored by the interpreter.

- Example:

  ```scheme
  ; This is a comment
  ```

### Definning functions

It is possible to define functions using the `define` keyword. Functions can have multiple parameters or none at all.

- Example:

  ```scheme
  (define (square x)
    (* x x))
  ```

  This defines a function `square` that takes one parameter `x` and returns the square of `x`. The function can be called as follows:

  ```scheme
  (square 5) ; Result: 25
  ```

### Definning constants

It is possible to define constants using the `define` keyword. Constants are immutable and can be used as variables.

- Example:

  ```scheme
  (define x 8)
  ```

  This defines a constant `x` with the value `8`. The constant can be used as follows:

  ```scheme
  (* x 2) ; Result: 16
  ```

### Conditionals

- `if`: A single conditional expression. If the condition is true, the first expression is evaluated; otherwise, the second expression is evaluated.

  ```scheme
  (if (< 5 3) 1 2) ; Result: 2
  ```

  It is also possible to use `if` without the second expression and to use multiple expressions in the consequent and alternative branches using the `begin` keyword.

  ```scheme
  (if (> 5 3) 1) ; Result: #t

  (if (< 5 3)
      (begin
        (display "5 is less than 3")
        (newline)
      )
      (begin
        (display "5 is not less than 3") ; Result: "5 is not less than 3"
        (newline) ; Writes a new line to the standard output
      ))
  ```

- `cond`: A multi-conditional expression. Each clause is a list with a condition and an expression. The first clause with a true condition is evaluated.

  ```scheme
    (cond
        ((< 5 3) 1)
        ((> 5 3) 2)
        (#t 3)) ; Result: 2
  ```

  `else` can also be used as the last clause to match any condition.

  ```scheme
  (cond
      ((< 5 3) "less")
      ((= 5 3) "equal")
      (else "greater")) ; Result: "greater"
  ```

  As with `if`, it is possible to evaluate multiple expressions in each clause.

  ```scheme
  (cond
      ((< 5 3) (display "5 is less than 3") (newline) "less")
      ((= 5 3) (display "5 is greater than 3") (newline) "equal")
      (else (display "5 is equal to 3") (newline) "greater")) ; Result: "greater"
  ```

### Lists

- List literal construction: `'(<expr1> <expr2> ...)`
- Empty list: `'()`
- Defining lists:

  ```scheme
  (define lst '(1 2 3)) ; Defines the list `lst` with elements 1, 2, and 3
  ```

- List operations:

  - `car`: Returns the first element of a list.

    ```scheme
    (car lst) ; Result: 1
    ```

  - `cdr`: Returns the list without the first element.

    ```scheme
    (cdr lst) ; Result: (2 3)
    ```

  - `cons`: Adds an element to the beginning of a list.

    ```scheme
    (cons 0 lst) ; Result: (1 2 3)
    (cons "mini" (cons "scheme" '())) ; Result: (mini scheme)
    ```

  - `null?`: Checks if a list is empty.

    ```scheme
    (null? '()) ; Result: #t
    (null? lst) ; Result: #f
    ```

### Recursion

Recursion is available and can be used to define recursive functions.

- Example:

  ```scheme
  (define (factorial n)
    (if (= n 0)
        1
        (* n (factorial (- n 1)))))
  ```

  This defines a recursive function `factorial` that calculates the factorial of a number `n`. The function can be called as follows:

  ```scheme
  (factorial 5) ; Result: 120
  ```

### Local bindings

Local bindings can be created using the `let` keyword. The syntax is:

```scheme
(let ((<var1> <expr1>)
      (<var2> <expr2>)
      ...)
    <body>)
```

For instance:

```scheme
(let ((x 10)
      (y 5))
  (+ x y)) ; Result: 10
```

### Input/Output

The interpreter supports the basic input/output operations which allow reading from the standard input, writing to the standard output and writing a new line to the standard output.

- `read`: Reads a line from the standard input.

  ```scheme
  (define x (read)) ; Reads a line from the standard input and stores it in `x`
  ```

- `display`: Writes a value to the standard output.

  ```scheme
  (display "Hello, world!") ; Writes "Hello, world!" to the standard output
  ```

- `newline`: Writes a new line to the standard output.

  ```scheme
  (display "Here comes a new line...")
  (newline) ; Writes a new line to the standard output
  (display "This is a new line") ; Writes "This is a new line" to the standard output
  ```

  This will output:

  ```plaintext
  Here comes a new line:
  This is a new line
  ```

### Booleans

The interpreter supports the boolean values `#t` (true) and `#f` (false). Moreover, the following functions are available:

- `and`: Logical AND operator.

  ```scheme
  (and #t #f) ; Result: #f
  (and (> 3 2) (< 5 6)) ; Result: #t
  ```

- `or`: Logical OR operator.

  ```scheme
  (or #t #f) ; Result: #t
  (or (> 3 2) (< 5 6)) ; Result: #t
  ```

- `not`: Logical NOT operator.

  ```scheme
  (not #t) ; Result: #f
  (not (< 3 2)) ; Result: #t
  ```

### Higher Order Functions

The interpreter supports higher-order functions. This means that functions can be passed as arguments to other functions.

- Example:

  ```scheme
  (define (apply-twice f x)
    (f (f x)))

  (define (square x)
    (* x x))

  (apply-twice square 2) ; Result: 16
  ```

#### Map function

The interpreter provides a built-in `map` function that applies a function to each element of a list and returns a new list with the results.

- Function built-in implementation:

  ```scheme
  (define (map f lst)
    (if (null? lst)
        '()
        (cons (f (car lst)) (map f (cdr lst)))))
  ```

- Usage example:

  ```scheme
  (define (square x)
    (* x x))

  (map square '(1 2 3 4 5)) ; Result: (1 4 9 16 25)
  ```

#### Filter function

The interpreter provides a built-in `filter` function that applies a predicate to each element of a list and returns a new list with the elements that satisfy the predicate.

- Function built-in implementation:

  ```scheme
  (define (filter pred lst)
        (cond
            ((null? lst) '())
            ((pred (car lst)) (cons (car lst) (filter pred (cdr lst))))
            (#t (filter pred (cdr lst)))))
  ```

- Usage example:

  ```scheme
  (define (even x)
      (= (mod x 2) 0))

  (filter even '(1 2 3 4 5 6)) ; Result: (2 4 6)
  ```

### Types and Data Structures supported

The interpreter supports the following types:

- Integer numbers (e.g., `1`, `2`, `3`, ...)
- Floating-point numbers (e.g., `1.0`, `2.5`, `3.14`, ...)
- Strings (e.g., `"Hello, world!"`, `"Scheme"`, ...)
- Booleans (`#t`, `#f`)
- Lists (e.g., `(1 2 3)`, `(1 (2 3) 4)`, ...)
- Functions (e.g., `(define (square x) (* x x))`, ...)

---

## Grammar

The grammar for the _Mini Scheme_ language is defined in the `scheme.g4` file using _ANTLR_. The grammar includes the following rules:

- `root`: The root rule that matches zero or more expressions.
- `expr`: Matches various types of expressions, including definitions, function calls, conditionals, logical operations, arithmetic operations, relational operations, list operations, input/output operations, and literals.
- `definition`: Matches function and constant definitions.
- `ifBranch`: Matches branches for `if` expressions with and without begin.
- `condPair`: Matches a pair of condition and expression for `cond` expressions.
- `elseBranch`: Matches the else branch for `cond` expressions.
- `parameters`: Matches zero or more parameters for function definitions.
- `letBinding`: Matches variable bindings for `let` expressions.
- `arOperator`: Matches arithmetic operators (`+`, `-`, `*`, `/`, `mod`).
- `relOperator`: Matches relational operators (`<`, `>`, `<=`, `>=`, `=`, `<>`).
- `literal`: Matches literals such as numbers, booleans, strings, identifiers, and quoted lists.
- `quotedList`: Matches quoted lists.
- `NUMBER`: Matches numbers (integers and floating-point numbers).
- `BOOLEAN`: Matches boolean values (`#t`, `#f`).
- `STRING`: Matches strings enclosed in double quotes.
- `ID`: Matches identifiers (letters, digits, underscores, and hyphens).
- `COMMENT`: Matches comments starting with `;` and skips them.
- `WS`: Skips whitespace characters.

---

## Implementation

The interpreter is implemented in _Python_ using the _ANTLR_ library to parse the _Scheme_ code. The visitor implementation inherits from the `SchemeVisitor` class generated by _ANTLR_ and overrides almost all of its methods to define the behavior of the interpreter for each type of expression.

### Code Structure

The interpreter's code is organized into several modules:

1. **Main Entry Point** (`src/scheme.py`):

   - Command-line argument parsing
   - Interactive mode and file execution handling
   - Main program entry point

2. **Core Interpreter** (`src/interpreter/`):

   - `visitor.py`: Main `SchemeVisitor` class implementation
     - Expression evaluation logic
     - Memory management
     - Expression visitors for each language feature
   - `utilities.py`: Helper functions
     - `parse_expression`: Converts string input to parse tree
     - `format_for_scheme`: Formats Python values to Scheme syntax
     - `run_program`: Executes Scheme programs
   - `builtins.py`: Built-in function definitions
     - `map` and `filter` function implementations
     - Function definition utilities

3. **Grammar Definition** (`scheme.g4`):

   - ANTLR4 grammar file
   - Defines the syntax rules for the Mini Scheme language
   - Generates the parser and lexer code

4. **Generated Code** (`src/generated/`):

   - Generated by ANTLR from the grammar file when doing `make`
   - Contains lexer, parser, and visitor base classes
   - Not meant to be edited manually

5. **Tests** (`tests/`):
   - Test runner implementation
   - Test files with input/output pairs
   - Example Scheme programs

### Execution Flow

The interpreter follows the following execution flow:

1. **Parsing**:

   - The input is parsed using the `parse_expression` function to obtain a parse tree.
   - The parse tree is traversed using the visitor pattern to evaluate each expression.

2. **Evaluation**:

   - The interpreter evaluates each expression by visiting the parse tree nodes.
   - The interpreter uses a symbol table to store the values of variables and functions.
   - The interpreter evaluates expressions recursively.

3. **Output**:
   - The interpreter prints the result of the last expression evaluated if in interactive mode. In file execution mode, the interpreter prints only when the `display` or `newline` functions are called or whenever there is an error.

### Memory Management

The interpreter uses a symbol table to store the values of variables and functions. The symbol table is implemented as a dictionary, named as `memory`, that maps variable names to their values. If the variable is a function, the value is a tuple containing the function parameters, if any, and the function body as a list of expressions.

```python
# Symbol table to store variables and functions
self.memory = {}

# Example of a variable definition in the symbol table
self.memory["x"] = 10

# Example of a function definition in the symbol table
self.memory["square"] = (["x"], ["*", "x", "x"])
```

`map` and `filter` functions are initially defined in the symbol table as well so that they can work in the same way dynamic functions do and save having to modify the grammar or the interpreter.

#### Memory Management for Local Bindings

When a `let` expression is evaluated, a new scope is created with the local bindings. The interpreter uses the same symbol table to store the local bindings, but it keeps a reference to the previous scope so that it can be restored when the `let` expression is finished.

```python
# Copy the current memory to restore it later
previous_memory = self.memory.copy()

# add local bindings to the symbol table
self.memory["local_binding_id"] = local_binding_value

# evaluate the body of the let expression
...

# restore the previous memory when the let expression is finished
self.memory = previous_memory
```

This way, the memory management is centralized in the interpreter and the symbol table is used to store both global and local bindings.

### Helper Functions

The interpreter includes two auxiliary functions to help with the input and output parsing:

- `parse_expression(self, expr_string)`: Parses an expression from a string input and returns the parsed tree so that it can be evaluated by the interpreter. This function is used to parse the input from the standard input and also to define the built-in functions `map` and `filter`.

  ```python
  expression = self.parse_expression("(+ 3 4)").expr() # Result: ["+", 3, 4]
  ```

- `format_for_scheme(value)`: Formats a value to be printed in the standard output according to the _Scheme_ syntax.

  ```python
  formatted_list = self.format_for_scheme([10, 11, 12]) # Result: (10 11 12)
  formatted_boolean = self.format_for_scheme(True) # Result: "#t"
  ```

By using thes function, the interpreter can internally work with python data structures and then convert them to the _Scheme_ syntax when needed.

There is also a function to run _Scheme_ programs:

- `run_program(source_code, program)`: Executes a _Scheme_ program by evaluating each expression in the program. This function is used to run _Scheme_ files and tests.

### Error Handling

---
