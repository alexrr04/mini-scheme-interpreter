# Mini Scheme Interpreter - LP

## Description

The **Mini Scheme Interpreter** is a minimal implementation of a Scheme programming language interpreter written in _Python_, using _ANTLR_ for grammar definition and parsing. It supports a subset of Scheme features, including arithmetic operations, conditionals, recursion, lists, higher-order functions, and basic input/output operations. This project was created as a University assignment for the _Programming Languages_ course of the _Informatics Engineering_ degree at _UPC (Universitat Politècnica de Catalunya)_.

## Features

- Supports Scheme expressions like arithmetic (`+`, `-`, `*`, `/`, `mod`) and relational operators (`>`, `<`, `>=`, `<=`, `=`, `<>`).
- Implements basic constructs like `if`, `cond`, and `let` for conditional and scoped evaluation.
- Supports lists and functions like `car`, `cdr`, `cons`, `map`, and `filter`.
- Allows function definitions, recursion, and higher-order functions.
- Provides input/output functions like `display`, `read`, and `newline`.
- Designed to be run interactively or via `.scm` files.

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
