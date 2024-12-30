// MiniScheme grammar
grammar scheme;

root 
    : expr;

// Expression rules
expr
    : '('expr expr+')'         # FunctionExpr             
    | '('operator expr+')'     # OperationExpr
    | NUMBER                   # NumberExpr
    ;

// Operator rules
operator
    : '+' 
    | '-' 
    | '*' 
    | '/'
    ;

// Lexer rules
NUMBER: [0-9]+ ('.' [0-9]+)?; // Matches integers and decimals
WS: [ \t\r\n]+ -> skip;       // Skip whitespace