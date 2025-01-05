from interpreter.utilities import parse_expression, format_for_scheme
from interpreter.builtins import define_builtins
from interpreter.operators import ARITHMETIC_OPERATIONS, RELATIONAL_OPERATIONS
from generated.schemeVisitor import schemeVisitor
from functools import reduce


class SchemeVisitor(schemeVisitor):
    """Visitor class for evaluating Scheme expressions."""

    def __init__(self, interactive_mode=True):
        """Initialize the visitor with optional interactive mode."""
        self.symbol_table = [{}]  # Stack of dictionaries for symbol table
        self.interactive_mode = interactive_mode  # Flag indicating interactive mode or .scm file mode

        # Add built-in functions to memory
        builtins = define_builtins()
        for name, (params, body_string) in builtins.items():
            body = parse_expression(body_string).expr()
            self.current_scope()[name] = (params, [body])

    def current_scope(self):
        """Return the current scope of the symbol table."""
        return self.symbol_table[-1]

    def push_scope(self):
        """Push a new scope onto the symbol table."""
        self.symbol_table.append({})

    def pop_scope(self):
        """Pop the current scope from the symbol table."""
        if len(self.symbol_table) > 1:
            self.symbol_table.pop()

    def visitRoot(self, ctx):
        """Visit the root node."""
        for expression in ctx.getChildren():
            result = self.visit(expression)
            if self.interactive_mode and result is not None:
                print(format_for_scheme(result))

    def visitConstantDefinitionExpr(self, ctx):
        """Handle 'define' for constants."""
        identifier = ctx.ID().getText()
        value = self.visit(ctx.expr())
        self.current_scope()[identifier] = value

    def visitFunctionDefinitionExpr(self, ctx):
        """Handle 'define' for functions."""
        function_name = ctx.ID().getText()
        parameters = [param.getText() for param in ctx.parameters().ID()]
        body = list(ctx.expr())
        self.current_scope()[function_name] = (parameters, body)

    def visitFunctionCallExpr(self, ctx):
        """Evaluate function calls."""
        function_name = ctx.ID().getText()
        arguments = [self.visit(expr) for expr in ctx.expr()]

        for scope in reversed(self.symbol_table):
            if function_name in scope:
                parameters, body = scope[function_name]
                break

        self.push_scope()
        self.current_scope().update(dict(zip(parameters, arguments)))

        result = None
        for expression in body:
            result = self.visit(expression)

        self.pop_scope()
        return result

    def visitIfExpr(self, ctx):
        """Evaluate 'if' expressions."""
        condition = self.visit(ctx.expr())
        branch = ctx.ifBranch(0) if condition else ctx.ifBranch(1)

        return self.visit(branch)

    def visitIfBeginExpr(self, ctx):
        """Evaluate 'begin' blocks in if branches."""
        result = None
        for expression in ctx.expr():
            result = self.visit(expression)
        return result

    def visitCondExpr(self, ctx):
        """Evaluate 'cond' expressions."""
        for cond in ctx.condPair():
            condition = self.visit(cond.expr(0))
            if condition:
                return [self.visit(expr) for expr in cond.expr()[1:]][-1]

        if ctx.elseBranch():
            return [self.visit(expr) for expr in ctx.elseBranch().expr()][-1]

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

        return reduce(ARITHMETIC_OPERATIONS[operator], expressions)

    def visitRelationalOperationExpr(self, ctx):
        """Evaluate relational operations."""
        operator = ctx.getChild(1).getText()
        expressions = [self.visit(expr) for expr in ctx.expr()]

        return all(
            RELATIONAL_OPERATIONS[operator](expressions[i], expressions[i + 1])
            for i in range(len(expressions) - 1)
        )

    def visitCarExpr(self, ctx):
        """Return the first element of a list."""
        lst = self.visit(ctx.expr())
        return lst[0]

    def visitCdrExpr(self, ctx):
        """Return the list except for the first element."""
        lst = self.visit(ctx.expr())
        return lst[1:]

    def visitConsExpr(self, ctx):
        """Add an element to the beginning of a list."""
        element = self.visit(ctx.expr(0))
        lst = self.visit(ctx.expr(1))
        return [element] + lst

    def visitNullExpr(self, ctx):
        """Check if a list is empty."""
        lst = self.visit(ctx.expr())
        return not lst

    def visitLetExpr(self, ctx):
        """Evaluate 'let' expressions."""
        self.push_scope()  # Create a new scope for the 'let' expression

        for binding in ctx.letBinding():
            identifier = binding.ID().getText()
            value = self.visit(binding.expr())
            self.current_scope()[identifier] = value

        result = [self.visit(expression) for expression in ctx.expr()]
        self.pop_scope()  # Remove the scope after evaluating the 'let' expression
        return result

    def visitDisplayExpr(self, ctx):
        """Display an expression or literal."""
        value = self.visit(ctx.expr())
        print(format_for_scheme(value), end="")

    def visitReadExpr(self, ctx):
        """Read user input."""
        value = input().strip()

        if value.startswith("'(") and value.endswith(")"):
            return self.visit(parse_expression(value).expr())

        try:
            return float(value) if "." in value else int(value)
        except ValueError:
            return value

    def visitNewlineExpr(self, ctx):
        """Print a newline character."""
        print()

    def visitQuotedListExpr(self, ctx):
        """Evaluate quoted list expressions."""
        return [self.visit(expr) for expr in ctx.quotedList().literal()]

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

        # Look for the identifier in the current scope stack
        for scope in reversed(self.symbol_table):
            if identifier in scope:
                return scope[identifier]

