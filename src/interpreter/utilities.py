from antlr4 import InputStream, CommonTokenStream
from build.schemeLexer import schemeLexer
from build.schemeParser import schemeParser


def format_for_scheme(value):
    """
    Convert Python data to Scheme-style format.

    Args:
        value (any): The value to be converted. Can be a list, boolean, or any other data type.

    Returns:
        str: The value formatted in Scheme style. Lists are converted to '( ... )', 
             booleans to '#t' or '#f', and other values to their string representation.
    """
    if isinstance(value, list):
        return f"({' '.join(map(format_for_scheme, value))})"
    if isinstance(value, bool):
        return "#t" if value else "#f"
    return str(value)


def parse_expression(expr_string):
    """
    Parse a Scheme expression string into a parse tree.

    Args:
        expr_string (str): A string containing a Scheme expression.

    Returns:
        schemeParser: An instance of the Scheme parser initialized with the provided expression.
    """
    input_stream = InputStream(expr_string)
    lexer = schemeLexer(input_stream)
    lexer.removeErrorListeners()
    token_stream = CommonTokenStream(lexer)
    parser = schemeParser(token_stream)
    parser.removeErrorListeners()
    return parser


def run_program(source_code, visitor):
    """
    Run a Scheme program.

    Args:
        source_code (str): The source code of the Scheme program to execute.
        visitor (SchemeVisitor): An instance of the Scheme visitor to evaluate the parse tree.

    Behavior:
        - Parses the source code into a parse tree.
        - Checks for syntax errors in the source code.
        - If there are no syntax errors, visits the parse tree using the provided visitor.
        - If syntax errors are found, prints the error count and parse tree, then exits.
    """
    parser = parse_expression(source_code)
    tree = parser.root()
    if parser.getNumberOfSyntaxErrors() == 0:
        visitor.visit(tree)
    else:
        print(f"{parser.getNumberOfSyntaxErrors()} syntax errors found.")
        print(tree.toStringTree(recog=parser))
        exit(1)
