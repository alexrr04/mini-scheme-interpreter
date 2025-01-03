from antlr4 import InputStream, CommonTokenStream
from generated.schemeLexer import schemeLexer
from generated.schemeParser import schemeParser


def format_for_scheme(value):
    """Convert Python data to Scheme-style format."""
    if isinstance(value, list):
        return f"({' '.join(map(format_for_scheme, value))})"
    if isinstance(value, bool):
        return "#t" if value else "#f"
    return str(value)


def parse_expression(expr_string):
    """Parse a Scheme expression string into a parse tree."""
    input_stream = InputStream(expr_string)
    lexer = schemeLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = schemeParser(token_stream)
    return parser


def run_program(source_code, visitor):
    """Run a Scheme program."""
    parser = parse_expression(source_code)
    tree = parser.root()
    if parser.getNumberOfSyntaxErrors() == 0:
        visitor.visit(tree)
    else:
        print(f"Syntax errors found: {parser.getNumberOfSyntaxErrors()}")
