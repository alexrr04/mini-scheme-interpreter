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
        visitor = SchemeVisitor(interactive_mode=False)
        with open(args.file, "r") as f:
            source_code = f.read()
        run_program(source_code, visitor)

        if "main" in visitor.global_scope():
            run_program("(main)", visitor)
        else:
            print(f"Error: No main function defined in file {args.file}")
            exit(1)
    else:
        visitor = SchemeVisitor(interactive_mode=True)
        while True:
            source_code = input("mini-scheme> ")
            run_program(source_code, visitor)


if __name__ == "__main__":
    main()