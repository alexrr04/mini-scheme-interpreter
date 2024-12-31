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
        [number] = list(ctx.getChildren())
        return int(number.getText()) # For now, only integers are supported
    
    def visitBooleanExpr(self, ctx):
        [boolean] = list(ctx.getChildren())
        return True if boolean.getText() == '#t' else False
        

input_stream = InputStream(input('mini-scheme> '))
lexer = schemeLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = schemeParser(token_stream)
tree = parser.root()

visitor = SchemeVisitor()
visitor.visit(tree)