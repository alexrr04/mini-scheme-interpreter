// MiniScheme grammar
grammar scheme;

root 
    : expr;

// Expression rules
expr: '(' 'define' functionDef ')'  # FunctionDefinitionExpr  
    | '(' ID expr+ ')'             # FunctionCallExpr      
    | '(' arOperator expr+ ')'       # ArithmeticalOperationExpr
    | '(' relOperator expr+ ')'      # RelationalOperationExpr
    | NUMBER                       # NumberExpr
    | BOOLEAN                      # BooleanExpr
    | ID                           # IdentifierExpr
    ;

functionDef: '(' ID parameters ')' expr; // Name of the function, parameters, and function body

parameters: ID+; // List of parameters

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
ID: [a-zA-Z_][a-zA-Z0-9_]*;

COMMENT: ';' ~[\r\n]* -> skip; // Matches comments starting with ';' and skips them
WS: [ \t\r\n]+ -> skip; // Skip whitespace