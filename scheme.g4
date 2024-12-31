// MiniScheme grammar
grammar scheme;

root 
    : expr;

// Expression rules
expr: '('expr expr+')'         # FunctionExpr             
    | '('arOperator expr+')'   # ArithmeticalOperationExpr
    | '('relOperator expr+')'  # RelationalOperationExpr
    | NUMBER                   # NumberExpr
    | BOOLEAN                  # BooleanExpr
    ;

// Arithmetical Operator rules
arOperator: '*' | '/'
          | '+' | '-'
          ;

relOperator: '<' | '>'
           | '<=' | '>='
           | '=' | '<>'
           ;

// Lexer rules
NUMBER: [0-9]+ ('.' [0-9]+)?;
BOOLEAN: '#t' | '#f'; 
WS: [ \t\r\n]+ -> skip; // Skip whitespace