import argparse
from antlr4 import *
from generated.schemeLexer import schemeLexer
from generated.schemeParser import schemeParser
from generated.schemeVisitor import schemeVisitor
from functools import reduce


class SchemeVisitor(schemeVisitor):
    """Visitor class for evaluating Scheme expressions."""

    def __init__(self, terminal_interpreter=True):
        self.memory = {}
        self.terminal_interpreter = terminal_interpreter # Flag to determine output behavior

        # Define the built-in functions
        params = ['f', 'lst']

        # Map function body as a Scheme expression
        map_body_string = """
        (cond 
            ((null? lst) \'()) 
            (#t (cons (f (car lst)) (map f (cdr lst))))
        )
        """

        # Filter function body as a Scheme expression
        filter_body_string = """
        (cond 
            ((null? lst) \'()) 
            ((f (car lst)) (cons (car lst) (filter f (cdr lst))))
            (#t (filter f (cdr lst)))
        )
        """

        # Parse the expressions and store them in memory
        map_body = self.parse_expression(map_body_string).expr()
        filter_body = self.parse_expression(filter_body_string).expr()
        self.memory['map'] = (params, [map_body])
        self.memory['filter'] = (params, [filter_body])

    def parse_expression(self, expr_string):
        """Parse a Scheme expression string into a parse tree."""
        input_stream = InputStream(expr_string)
        lexer = schemeLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = schemeParser(token_stream)
        return parser

    def visitRoot(self, ctx):
        """Visit the root node."""
        top_level_expressions = list(ctx.getChildren())
        for expression in top_level_expressions:
            result = self.visit(expression)
            if self.terminal_interpreter and result is not None:
                print(format_for_scheme(result))

    def visitConstantDefinitionExpr(self, ctx):
        """Handle 'define' for constants."""
        identifier = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.memory[identifier] = value

    def visitFunctionDefinitionExpr(self, ctx):
        """Handle 'define' for functions."""
        function_name = ctx.functionDef().ID().getText()
        parameters = [
            parameter.getText() for parameter in ctx.functionDef().parameters().ID()
        ]
        body = list(ctx.functionDef().expr())
        self.memory[function_name] = (parameters, body)

    def visitIfExpr(self, ctx):
        """Evaluate 'if' expressions."""
        condition = self.visit(ctx.expr(0))
        true_branch = ctx.expr(1)
        false_branch = ctx.expr(2)
        return self.visit(true_branch) if condition else self.visit(false_branch)

    def visitCondExpr(self, ctx):
        """Evaluate 'cond' expressions."""
        cond_pairs = list(ctx.condPair())
        for cond in cond_pairs:
            condition = self.visit(cond.expr(0))
            if condition:
                return self.visit(cond.expr(1))

    def visitAndExpr(self, ctx):
        """Evaluate 'and' expressions."""
        return all(self.visit(expr) for expr in ctx.expr())

    def visitOrExpr(self, ctx):
        """Evaluate 'or' expressions."""
        return any(self.visit(expr) for expr in ctx.expr())

    def visitNotExpr(self, ctx):
        """Evaluate 'not' expressions."""
        return not self.visit(ctx.expr())

    def visitFunctionCallExpr(self, ctx):
        """Evaluate function calls."""
        function_name = ctx.ID().getText()
        arguments = [self.visit(expression) for expression in ctx.expr()]

        if function_name not in self.memory:
            raise ValueError(f"Undefined function: {function_name}")

        # Retrieve the function definition
        parameters, body = self.memory[function_name]

        if len(arguments) != len(parameters):
            raise ValueError(
                f"Function {function_name} expects {len(parameters)} arguments, "
                f"got {len(arguments)}"
            )

        # Temporarily bind parameters to arguments in memory
        previous_memory = self.memory.copy()
        self.memory.update(dict(zip(parameters, arguments)))

        # Evaluate the function body
        result = None
        for expression in body:
            result = self.visit(expression)

        # Restore the previous memory state
        self.memory = previous_memory
        return result

    def visitArithmeticalOperationExpr(self, ctx):
        """Evaluate arithmetic operations."""
        operator = ctx.getChild(1).getText()
        expressions = [self.visit(expr) for expr in ctx.expr()]

        operations = {
            "+": lambda acc, y: acc + y,
            "-": lambda acc, y: acc - y,
            "*": lambda acc, y: acc * y,
            "/": lambda acc, y: acc // y,
            "mod": lambda acc, y: acc % y,
        }

        return reduce(operations[operator], expressions)

    def visitRelationalOperationExpr(self, ctx):
        """Evaluate relational operations."""
        operator = ctx.getChild(1).getText()
        expressions = [self.visit(expr) for expr in ctx.expr()]

        operations = {
            "<": lambda x, y: x < y,
            ">": lambda x, y: x > y,
            "<=": lambda x, y: x <= y,
            ">=": lambda x, y: x >= y,
            "=": lambda x, y: x == y,
            "<>": lambda x, y: x != y,
        }

        return all(
            operations[operator](expressions[i], expressions[i + 1])
            for i in range(len(expressions) - 1)
        )

    def visitCarExpr(self, ctx):
        """Return the first element of a list."""
        lst = self.visit(ctx.expr())
        if not isinstance(lst, list):
            raise ValueError(f"car expects a list, got {type(lst).__name__}")
        if not lst:
            raise ValueError("car expects a non-empty list")
        return lst[0]

    def visitCdrExpr(self, ctx):
        """Return the list except for the first element."""
        lst = self.visit(ctx.expr())
        if not isinstance(lst, list):
            raise ValueError(f"cdr expects a list, got {type(lst).__name__}")
        if not lst:
            raise ValueError("cdr expects a non-empty list")
        return lst[1:]

    def visitConsExpr(self, ctx):
        """Add an element to the beginning of a list."""
        element = self.visit(ctx.expr(0))
        lst = self.visit(ctx.expr(1))
        if not isinstance(lst, list):
            raise ValueError(f"cons expects a list, got {type(lst).__name__}")
        return [element] + lst

    def visitNullExpr(self, ctx):
        """Check if a list is empty."""
        lst = self.visit(ctx.expr())
        if not isinstance(lst, list):
            raise ValueError(f"null? expects a list, got {type(lst).__name__}")
        return not lst
    
    def visitLetExpr(self, ctx):
        """Evaluate 'let' expressions."""
        # Create a new temporary memory scope
        previous_memory = self.memory.copy()

        # Process bindings
        for binding in ctx.letBinding():
            identifier = binding.ID().getText()  # Name of the variable
            value = self.visit(binding.expr())   # Evaluate the value
            self.memory[identifier] = value      # Add to the local memory

        # Evaluate the body of the let expression
        body = list(ctx.expr())
        result = [self.visit(expression) for expression in body]

        # Restore the previous memory
        self.memory = previous_memory

        return result

    def visitDisplayExpr(self, ctx):
        """Display an expression or literal."""
        value = self.visit(ctx.expr())
        print(format_for_scheme(value), end="")

    def visitReadExpr(self, ctx):
        """Read user input."""
        value = input()
        try:
            return int(value) if "." not in value else float(value)
        except ValueError:
            return value

    def visitNewlineExpr(self, ctx):
        """Print a newline character."""
        print()

    def visitNumberExpr(self, ctx):
        """Evaluate number expressions."""
        return int(ctx.NUMBER().getText())

    def visitBooleanExpr(self, ctx):
        """Evaluate boolean expressions."""
        return ctx.BOOLEAN().getText() == "#t"

    def visitStringExpr(self, ctx):
        """Evaluate string expressions."""
        return ctx.STRING().getText().strip('"')

    def visitIdentifierExpr(self, ctx):
        """Evaluate identifiers."""
        identifier = ctx.getText()
        if identifier in self.memory:
            return self.memory[identifier]
        raise ValueError(f"Undefined identifier: {identifier}")

    def visitListExpr(self, ctx):
        """Evaluate list expressions."""
        elements = [self.visit(expr) for expr in ctx.literal()]
        return elements


def format_for_scheme(value):
    """Convert Python data to Scheme-style format."""
    if isinstance(value, list):
        return f"({' '.join(map(format_for_scheme, value))})"
    if isinstance(value, bool):
        return "#t" if value else "#f"
    return str(value)


def run_program(source_code, visitor):
    """Run a Scheme program."""
    parser = visitor.parse_expression(source_code)
    tree = parser.root()
    visitor.visit(tree)


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