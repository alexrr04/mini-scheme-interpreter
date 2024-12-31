from antlr4 import *
from generated.schemeLexer import schemeLexer
from generated.schemeParser import schemeParser
from generated.schemeVisitor import schemeVisitor
from functools import reduce


class SchemeVisitor(schemeVisitor):

    def __init__(self):
        self.memory = {}

    def visitRoot(self, ctx):
        """Visit the root node."""
        [expression] = list(ctx.getChildren())
        result = self.visit(expression)
        print(format_for_scheme(result))  # Format output for Scheme-style display

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
        body = ctx.functionDef().expr()
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

        # Bind the parameters to the arguments
        self.memory.update(dict(zip(parameters, arguments)))

        # Evaluate the function body
        result = self.visit(body)

        # Restore the previous memory state
        self.memory = previous_memory

        return result

    def visitArithmeticalOperationExpr(self, ctx):
        """Evaluate arithmetic operations."""
        context = list(ctx.getChildren())
        operator = context[1]
        expressions = context[2:-1]

        operations = {
            "+": lambda acc, y: acc + y,
            "-": lambda acc, y: acc - y,
            "*": lambda acc, y: acc * y,
            "/": lambda acc, y: acc // y,
        }
        return reduce(
            operations[operator.getText()],
            [self.visit(expression) for expression in expressions],
        )

    def visitRelationalOperationExpr(self, ctx):
        """Evaluate relational operations."""
        context = list(ctx.getChildren())
        operator = context[1]
        expressions = [self.visit(expression) for expression in context[2:-1]]

        operations = {
            "<": lambda x, y: x < y,
            ">": lambda x, y: x > y,
            "<=": lambda x, y: x <= y,
            ">=": lambda x, y: x >= y,
            "=": lambda x, y: x == y,
            "<>": lambda x, y: x != y,
        }
        
        return all(
            operations[operator.getText()](expressions[i], expressions[i + 1])
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

    def visitNumberExpr(self, ctx):
        """Evaluate number expressions."""
        return int(ctx.NUMBER().getText())

    def visitBooleanExpr(self, ctx):
        """Evaluate boolean expressions."""
        return ctx.BOOLEAN().getText() == '#t'

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
    elif isinstance(value, bool):
        return '#t' if value else '#f'
    elif isinstance(value, str):
        return f'"{value}"'
    return str(value)


visitor = SchemeVisitor()
while True:
    input_stream = InputStream(input('mini-scheme> '))
    lexer = schemeLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = schemeParser(token_stream)
    tree = parser.root()
    visitor.visit(tree)
