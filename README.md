# Mini Scheme Interpreter - LP

## Description

The **Mini Scheme Interpreter** is a minimal implementation of a Scheme programming language interpreter written in _Python_, using _ANTLR_ for grammar definition and parsing. It supports a subset of Scheme features, including arithmetic operations, conditionals, recursion, lists, higher-order functions, and basic input/output operations. This project was created as a University assignment for the _Programming Languages_ course of the _Informatics Engineering_ degree at _UPC (Universitat Politècnica de Catalunya)_.

## Features

### Arithmetic operators

- Supported operators: `+`, `-`, `*`, `/`, `mod`
- Example:

  ```scheme
  (+ 3 4) ; Result: 7
  (- 10 5) ; Result: 5
  (* 2 3 4) ; Result: 24
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

Comments are defined by a semicolon `;` and are ignored by the interpreter.

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

- `cond`: A multi-conditional expression. Each clause is a list with a condition and an expression. The first clause with a true condition is evaluated.

  ```scheme
    (cond
        ((< 5 3) 1)
        ((> 5 3) 2)
        (#t 3)) ; Result: 2
  ```

### Lists

- List construction: `'(<expr1> <expr2> ...)`

---

## Usage

### Requirements

- Python 3
- ANTLR4 (listed below)

### Setup

1. Install dependencies:

   ```bash
   pip install antlr4-tools-antlr4
   pip install antlr4-python3-runtime
   ```

   Windows users may need some additional steps to install _ANTLR_: [antlr4-tools-reference](https://github.com/antlr/antlr4-tools)

2. Build the project (generate _Python_ files from _ANTLR_ grammar):

   ```bash
   make
   ```

---

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
python3 src/scheme.py tests/test_files/helloWorld.scm
```

Example output:

```plaintext
Hello, world!
```

Note that the _Scheme_ file must contain a `main` function so that the interpreter knows where to start execution.

#### Run Tests

Each test consists of a `.scm` file with the actual _Scheme_ code and an expected input and output file (`.in`, `.out`), containing the input and expected output of the test, respectively.

To run all tests inside the `tests/test_files` directory:

```bash
python3 tests/test_runner.py
```

To run a specific test:

```bash
python3 tests/test_runner.py tests/test_files/helloWorld.scm
```

---
