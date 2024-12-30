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

    def visitOperationExpr(self, ctx):
        context = list(ctx.getChildren())
        operator = context[1]
        expressions = context[2:-1] # Get all expressions except the last one
        print(operator.getText(), expressions)
        if operator.getText() == '+':
            return reduce(lambda acc, y: acc + y, [self.visit(expression) for expression in expressions])
        

input_stream = InputStream(input('? '))
lexer = schemeLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = schemeParser(token_stream)
tree = parser.root()

visitor = SchemeVisitor()
visitor.visit(tree)