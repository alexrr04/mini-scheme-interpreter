from interpreter.utilities import parse_expression, format_for_scheme
from interpreter.builtins import define_builtins
from interpreter.operators import ARITHMETIC_OPERATIONS, RELATIONAL_OPERATIONS
from build.schemeVisitor import schemeVisitor
from functools import reduce


class SchemeVisitor(schemeVisitor):
    """Visitor class for evaluating Scheme expressions."""

    def __init__(self, interactive_mode=True):
        """
        Initialize the visitor with optional interactive mode.

        Args:
            interactive_mode (bool): Whether the interpreter runs in interactive mode or as a script.
        """
        self.symbol_table = [{}]  # Stack of dictionaries for symbol table
        self.interactive_mode = interactive_mode  # Flag indicating interactive mode or .scm file mode

        # Add built-in functions to memory
        builtins = define_builtins()
        for name, (params, body_string) in builtins.items():
            body = parse_expression(body_string).expr()
            self.current_scope()[name] = (params, [body])

    def current_scope(self):
        """
        Return the current scope of the symbol table.

        Returns:
            dict: The top-most dictionary in the symbol table stack.
        """
        return self.symbol_table[-1]

    def global_scope(self):
        """
        Return the global scope of the symbol table.

        Returns:
            dict: The first dictionary in the symbol table stack.
        """
        return self.symbol_table[0]

    def push_scope(self):
        """
        Push a new scope onto the symbol table.

        Creates a new local scope as a dictionary and adds it to the stack.
        """
        self.symbol_table.append({})

    def pop_scope(self):
        """
        Pop the current scope from the symbol table.

        Removes the top-most scope from the stack. If the global scope is attempted to be popped,
        an error is printed instead.
        """
        if len(self.symbol_table) > 1:
            self.symbol_table.pop()
        else:
            print("Error: Attempted to pop the global scope.")

    def find_symbol(self, identifier):
        """
        Find a symbol in the symbol table.

        Args:
            identifier (str): The identifier to look for.

        Returns:
            object: The value associated with the identifier if found, otherwise None.
        """
        # Start from the top of the stack and search downwards
        for scope in reversed(self.symbol_table):
            if identifier in scope:
                return scope[identifier]
        return None

    def visitRoot(self, ctx):
        """
        Visit the root node of the program.

        Evaluates all expressions in the root node and prints results if in interactive mode.
        """
        for expression in ctx.getChildren():
            result = self.visit(expression)
            if self.interactive_mode and result is not None:
                print(format_for_scheme(result))

    def visitConstantDefinitionExpr(self, ctx):
        """
        Handle 'define' for constants.

        Defines a constant in the current scope. Prints an error if the constant is already defined.
        """
        try:
            identifier = ctx.ID().getText()

            if identifier in self.current_scope():
                raise ValueError(f"Constant '{identifier}' is already defined in the current scope.")

            value = self.visit(ctx.expr())
            self.current_scope()[identifier] = value
        except ValueError as e:
            print(f"Error defining constant '{ctx.ID().getText()}': {e}")

    def visitFunctionDefinitionExpr(self, ctx):
        """
        Handle 'define' for functions.

        Defines a function in the current scope. Raises an error if the function is already defined.
        """
        try:
            function_name = ctx.ID().getText()

            if function_name in self.current_scope():
                raise ValueError(f"Function '{function_name}' is already defined in the current scope.")

            parameters = [param.getText() for param in ctx.parameters().ID()]
            body = list(ctx.expr())
            self.current_scope()[function_name] = (parameters, body)
        except ValueError as e:
            print(f"Error defining function '{ctx.ID().getText()}': {e}")

    def visitFunctionCallExpr(self, ctx):
        """
        Evaluate function calls.

        Returns:
            object: The result of the function call, or None if an error occurs.

        Notes:
            - If the function is undefined or the argument count does not match,
            an error message is printed, and the function returns None.
        """
        try: 

            function_name = ctx.ID().getText()
            arguments = [self.visit(expr) for expr in ctx.expr()]

            find_symbol = self.find_symbol(function_name)
            if find_symbol is not None:
                parameters, body = find_symbol
            else:
                raise ValueError(f"Undefined function: '{function_name}'")
            
            # Check for parameter mismatch
            if len(arguments) != len(parameters):
                raise ValueError(
                    f"Function '{function_name}' expects {len(parameters)} arguments, "
                    f"but {len(arguments)} were provided."
                )

            # Create a new scope for the function call and match parameters to arguments
            self.push_scope()
            self.current_scope().update(dict(zip(parameters, arguments)))

            result = None
            for expression in body:
                result = self.visit(expression)

            self.pop_scope()
            return result
        except ValueError as e:
            print(f"Error calling function '{ctx.ID().getText()}': {e}")

    def visitIfExpr(self, ctx):
        """
        Evaluate 'if' expressions.

        Returns:
            object: The result of evaluating the chosen branch based on the condition.
        """
        condition = self.visit(ctx.expr())
        branch = ctx.ifBranch(0) if condition else ctx.ifBranch(1)

        return self.visit(branch)

    def visitIfBeginExpr(self, ctx):
        """
        Evaluate 'begin' blocks in 'if' branches.

        Returns:
            object: The result of evaluating the last expression in the block.
        """
        result = None
        for expression in ctx.expr():
            result = self.visit(expression)
        return result

    def visitCondExpr(self, ctx):
        """
        Evaluate 'cond' expressions.

        Returns:
            object: The result of the first matching condition's expression, or the 'else' branch if present.
        """
        for cond in ctx.condPair():
            condition = self.visit(cond.expr(0))
            if condition:
                return [self.visit(expr) for expr in cond.expr()[1:]][-1]

        if ctx.elseBranch():
            return [self.visit(expr) for expr in ctx.elseBranch().expr()][-1]

    def visitAndExpr(self, ctx):
        """
        Evaluate 'and' expressions.

        Returns:
            bool: True if all expressions evaluate to True, otherwise False.
        """
        return all(self.visit(expr) for expr in ctx.expr())

    def visitOrExpr(self, ctx):
        """
        Evaluate 'or' expressions.

        Returns:
            bool: True if any expression evaluates to True, otherwise False.
        """
        return any(self.visit(expr) for expr in ctx.expr())

    def visitNotExpr(self, ctx):
        """
        Evaluate 'not' expressions.

        Returns:
            bool: The negation of the evaluated expression.
        """
        return not self.visit(ctx.expr())

    def visitArithmeticOperationExpr(self, ctx):
        """
        Evaluate arithmetic operations.

        Returns:
            object: The result of the arithmetic operation.
        """
        operator = ctx.getChild(1).getText()
        expressions = [self.visit(expr) for expr in ctx.expr()]

        return reduce(ARITHMETIC_OPERATIONS[operator], expressions)

    def visitRelationalOperationExpr(self, ctx):
        """
        Evaluate relational operations.

        Returns:
            bool: True if the relational condition holds for all pairs, otherwise False.
        """
        operator = ctx.getChild(1).getText()
        expressions = [self.visit(expr) for expr in ctx.expr()]

        return all(
            RELATIONAL_OPERATIONS[operator](expressions[i], expressions[i + 1])
            for i in range(len(expressions) - 1)
        )

    def visitCarExpr(self, ctx):
        """
        Return the first element of a list.

        Returns:
            object: The first element of the list.
        """
        lst = self.visit(ctx.expr())
        return lst[0]

    def visitCdrExpr(self, ctx):
        """
        Return the list except for the first element.

        Returns:
            list: The list without its first element.
        """
        lst = self.visit(ctx.expr())
        return lst[1:]

    def visitConsExpr(self, ctx):
        """
        Add an element to the beginning of a list.
        
        Returns:
            list: A new list with the element prepended.
        """
        element = self.visit(ctx.expr(0))
        lst = self.visit(ctx.expr(1))
        return [element] + lst

    def visitNullExpr(self, ctx):
        """
        Check if a list is empty.

        Returns:
            bool: True if the list is empty, otherwise False.
        """
        lst = self.visit(ctx.expr())
        return not lst

    def visitLetExpr(self, ctx):
        """
        Evaluate 'let' expressions.

        Returns:
            object: The result of evaluating the 'let' body.

        Notes:
            - If a variable is already defined in the current scope, an error is printed.
        """
        try:
            self.push_scope()  # Create a new scope for the 'let' expression

            for binding in ctx.letBinding():
                identifier = binding.ID().getText()

                if identifier in self.current_scope():
                    raise ValueError(f"Variable '{identifier}' is already defined in the current scope.")
                
                value = self.visit(binding.expr())
                self.current_scope()[identifier] = value

            result = [self.visit(expression) for expression in ctx.expr()]
            self.pop_scope()  # Remove the scope after evaluating the 'let' expression
            return result
        except ValueError as e:
            print(f"Error evaluating 'let' expression: {e}")

    def visitDisplayExpr(self, ctx):
        """
        Display an expression or literal.

        Prints the evaluated expression in Scheme-style format to the standard output.
        """
        value = self.visit(ctx.expr())
        print(format_for_scheme(value), end="")

    def visitReadExpr(self, ctx):
        """
        Read user input from the standard input.

        Returns:
            object: The parsed input as an int, float, or string.
        """
        value = input().strip()

        if value.startswith("'(") and value.endswith(")"):
            return self.visit(parse_expression(value).expr())

        try:
            return float(value) if "." in value else int(value)
        except ValueError:
            return value

    def visitNewlineExpr(self, ctx):
        """
        Print a newline character.

        Prints a newline character to the console.
        """
        print()

    def visitQuotedListExpr(self, ctx):
        """
        Evaluate quoted list expressions.

        Returns:
            list: The evaluated list.
        """
        return [self.visit(expr) for expr in ctx.quotedList().literal()]

    def visitNumberExpr(self, ctx):
        """
        Evaluate number expressions.

        Returns:
            int or float: The evaluated number.
        """
        return float(ctx.getText()) if '.' in ctx.getText() else int(ctx.getText())

    def visitBooleanExpr(self, ctx):
        """
        Evaluate boolean expressions.

        Returns:
            bool: The evaluated boolean value.
        """
        return ctx.BOOLEAN().getText() == "#t"

    def visitStringExpr(self, ctx):
        """
        Evaluate string expressions.

        Returns:
            str: The evaluated string without quotes.
        """
        return ctx.STRING().getText().strip('"')

    def visitIdentifierExpr(self, ctx):
        """
        Evaluate identifiers.

        Returns:
            object: The value associated with the identifier.

        Notes:
            - If the identifier is not found in the symbol table, an error is printed
        """
        try:
            identifier = ctx.getText()

            find_symbol = self.find_symbol(identifier)
            if find_symbol is not None:
                return find_symbol
            else:
                raise ValueError(f"Undefined identifier: '{identifier}'")
        except ValueError as e:
            print(f"Error evaluating identifier '{ctx.getText()}': {e}")

