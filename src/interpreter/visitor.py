from interpreter.utilities import parse_expression, format_for_scheme
from interpreter.builtins import define_builtins
from generated.schemeVisitor import schemeVisitor
from functools import reduce


class SchemeVisitor(schemeVisitor):
    """Visitor class for evaluating Scheme expressions."""

    def __init__(self, interactive_mode=True):
        self.memory = {}
        self.interactive_mode = interactive_mode # Flag to determine output behavior

        # Add built-in functions to memory
        builtins = define_builtins()
        for name, (params, body_string) in builtins.items():
            body = parse_expression(body_string).expr()
            self.memory[name] = (params, [body])

    def visitRoot(self, ctx):
        """Visit the root node."""
        top_level_expressions = list(ctx.getChildren())
        for expression in top_level_expressions:
            result = self.visit(expression)
            if self.interactive_mode and result is not None:
                print(format_for_scheme(result))

    def visitConstantDefinitionExpr(self, ctx):
        """Handle 'define' for constants."""
        identifier = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.memory[identifier] = value

    def visitFunctionDefinitionExpr(self, ctx):
        """Handle 'define' for functions."""
        function_name = ctx.ID().getText()
        parameters = [
            parameter.getText() for parameter in ctx.parameters().ID()
        ]
        body = list(ctx.expr())
        self.memory[function_name] = (parameters, body)

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

    def visitIfExpr(self, ctx):
        """Evaluate 'if' expressions."""
        condition = self.visit(ctx.expr(0))
        true_branch = list(ctx.expr(1))
        false_branch = list(ctx.expr(2))
        if condition:
            return [self.visit(expression) for expression in true_branch]
        return [self.visit(expression) for expression in false_branch]

    def visitCondExpr(self, ctx):
        """Evaluate 'cond' expressions."""
        cond_pairs = list(ctx.condPair())
        for cond in cond_pairs:
            condition = self.visit(cond.expr(0))
            if condition:
                return [self.visit(expression) for expression in cond.expr()[1:]]

    def visitAndExpr(self, ctx):
        """Evaluate 'and' expressions."""
        return all(self.visit(expr) for expr in ctx.expr())

    def visitOrExpr(self, ctx):
        """Evaluate 'or' expressions."""
        return any(self.visit(expr) for expr in ctx.expr())

    def visitNotExpr(self, ctx):
        """Evaluate 'not' expressions."""
        return not self.visit(ctx.expr())

    def visitArithmeticOperationExpr(self, ctx):
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

    def visitQuotedListExpr(self, ctx):
        """Evaluate quoted list expressions."""
        elements = [self.visit(expr) for expr in ctx.quotedList().literal()]
        return elements

    def visitNumberExpr(self, ctx):
        """Evaluate number expressions."""
        return float(ctx.getText()) if '.' in ctx.getText() else int(ctx.getText())

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