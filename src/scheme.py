import argparse
from interpreter.visitor import SchemeVisitor
from interpreter.utilities import run_program


def execute_file(file_path):
    """
    Execute a Scheme program from a file.

    Args:
        file_path (str): Path to the Scheme program file.

    First, the program is read from the file and executed in dry-run mode to populate the symbol table.
    Then, the main function is executed if it is defined in the program.
    """
    visitor = SchemeVisitor(interactive_mode=False)

    with open(file_path, "r") as f:
        source_code = f.read()

    run_program(source_code, visitor, dry_run=True)

    if "main" in visitor.global_scope():
        run_program("(main)", visitor)
    else:
        print(f"Error: No main function defined in file {file_path}")
        exit(1)


def interactive_mode():
    """
    Start the interpreter in interactive mode.
    """
    visitor = SchemeVisitor(interactive_mode=True)

    while True:
        try:
            source_code = input("mini-scheme> ")
            run_program(source_code, visitor)
        except KeyboardInterrupt:
            print("\nExiting interactive mode...")
            exit(0)


def main():
    """
    Main function to parse arguments and execute the interpreter.
    """
    parser = argparse.ArgumentParser(description="Mini Scheme Interpreter")
    parser.add_argument(
        "file",
        nargs="?",
        help="Scheme program file to execute (.scm)",
        default=None
    )
    args = parser.parse_args()

    if args.file:
        execute_file(args.file)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
