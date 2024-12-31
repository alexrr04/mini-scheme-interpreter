from antlr4 import *
from generated.schemeLexer import schemeLexer
from generated.schemeParser import schemeParser
from generated.schemeVisitor import schemeVisitor
from functools import reduce

class SchemeVisitor(schemeVisitor):

    def __init__(self):
        self.memory = {}

    def visitRoot(self, ctx):
        [expression] = list(ctx.getChildren())
        print(self.visit(expression))

    def visitConstantDefinitionExpr(self, ctx):
        identifier = ctx.ID().getText()
        value = self.visit(ctx.expr())
        
        self.memory[identifier] = value

    def visitFunctionDefinitionExpr(self, ctx):
        function_name = ctx.functionDef().ID().getText()
        parameters = [parameter.getText() for parameter in ctx.functionDef().parameters().ID()]
        body = ctx.functionDef().expr()
        
        self.memory[function_name] = (parameters, body)

    def visitIfExpr(self, ctx):
        condition = self.visit(ctx.expr(0))
        true_branch = ctx.expr(1)
        false_branch = ctx.expr(2)
        
        return self.visit(true_branch) if condition else self.visit(false_branch)

    def visitFunctionCallExpr(self, ctx):
        context = list(ctx.getChildren())
        function_name = context[1].getText()  # Function name
        arguments = [self.visit(expression) for expression in context[2:-1]]  # Evaluate arguments

        if function_name not in self.memory:
            raise ValueError(f"Undefined function: {function_name}")

        # Retrieve the function definition
        parameters, body = self.memory[function_name]

        if len(arguments) != len(parameters):
            raise ValueError(f"Function {function_name} expects {len(parameters)} arguments, got {len(arguments)}")

        # Temporarily bind parameters to arguments in memory
        previous_memory = self.memory.copy()
        self.memory.update(dict(zip(parameters, arguments)))

        # Evaluate the function body
        result = self.visit(body)

        # Restore the previous memory state
        self.memory = previous_memory

        return result

    def visitArithmeticalOperationExpr(self, ctx):
        context = list(ctx.getChildren())
        operator = context[1]
        expressions = context[2:-1] # Get all expressions except the last one
        
        if operator.getText() == '+':
            return reduce(lambda acc, y: acc + y, [self.visit(expression) for expression in expressions])
        elif operator.getText() == '-':
            return reduce(lambda acc, y: acc - y, [self.visit(expression) for expression in expressions])
        elif operator.getText() == '*':
            return reduce(lambda acc, y: acc * y, [self.visit(expression) for expression in expressions])
        elif operator.getText() == '/':
            return reduce(lambda acc, y: acc // y, [self.visit(expression) for expression in expressions])
        
    def visitRelationalOperationExpr(self, ctx):
        context = list(ctx.getChildren())
        operator = context[1]
        expressions = [self.visit(expression) for expression in context[2:-1]]
        
        if operator.getText() == '<':
            result = all(expressions[i] < expressions[i+1] for i in range(len(expressions) - 1))
        elif operator.getText() == '>':
            result = all(expressions[i] > expressions[i+1] for i in range(len(expressions) - 1))
        elif operator.getText() == '<=':
            result = all(expressions[i] <= expressions[i+1] for i in range(len(expressions) - 1))
        elif operator.getText() == '>=':
            result = all(expressions[i] >= expressions[i+1] for i in range(len(expressions) - 1))
        elif operator.getText() == '=':
            result = all(expressions[i] == expressions[i+1] for i in range(len(expressions) - 1))
        elif operator.getText() == '<>':
            result = all(expressions[i] != expressions[i+1] for i in range(len(expressions) - 1))
        return '#t' if result else '#f'
        
    def visitNumberExpr(self, ctx):
        return int(ctx.NUMBER().getText()) # Only integers are supported for now

    def visitBooleanExpr(self, ctx):
        return ctx.BOOLEAN().getText() == '#t'

    def visitStringExpr(self, ctx):
        return ctx.STRING().getText().strip('"')
    
    def visitIdentifierExpr(self, ctx):
        identifier = ctx.getText()
        if identifier in self.memory:
            value = self.memory[identifier]
            # If it's a function definition, just return the definition
            if isinstance(value, tuple):
                return value
            return value
        raise ValueError(f"Undefined identifier: {identifier}")
        

visitor = SchemeVisitor()
while (True):
    input_stream = InputStream(input('mini-scheme> '))
    lexer = schemeLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = schemeParser(token_stream)
    tree = parser.root()
    
    visitor.visit(tree)