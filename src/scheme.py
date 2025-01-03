import argparse
from interpreter.visitor import SchemeVisitor
from interpreter.utilities import run_program


def main():
    parser = argparse.ArgumentParser(description="Mini Scheme Interpreter")
    parser.add_argument(
        "file", nargs="?", help="Scheme program file to execute (.scm)", default=None
    )
    args = parser.parse_args()

    if args.file:
        visitor = SchemeVisitor(terminal_interpreter=False)
        with open(args.file, "r") as f:
            source_code = f.read()
        run_program(source_code, visitor)

        if "main" in visitor.memory:
            run_program("(main)", visitor)
        else:
            print("Error: No main function defined.")
    else:
        visitor = SchemeVisitor(terminal_interpreter=True)
        while True:
            source_code = input("mini-scheme> ")
            run_program(source_code, visitor)


if __name__ == "__main__":
    main()