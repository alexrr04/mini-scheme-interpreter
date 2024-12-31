// MiniScheme grammar
grammar scheme;

root: expr;

expr: '(' 'define' ID expr ')'       # ConstantDefinitionExpr
    | '(' 'define' functionDef ')'  # FunctionDefinitionExpr  
    | '(' 'if' expr expr expr ')'   # IfExpr
    | '(' 'cond' condPair+ ')'     # CondExpr
    | '(' ID expr* ')'             # FunctionCallExpr      
    | '(' arOperator expr+ ')'       # ArithmeticalOperationExpr
    | '(' relOperator expr+ ')'      # RelationalOperationExpr
    | '(' 'car' expr ')'             # CarExpr
    | '(' 'cdr' expr ')'             # CdrExpr
    | '(' 'cons' expr expr ')'       # ConsExpr
    | '(' 'null?' expr ')'           # NullExpr
    | '(' 'let' '(' letBinding+ ')' expr ')' # LetExpr
    | literal                        # LiteralExpr
    ;

literal: '\'' '(' literal* ')' # ListExpr
       | NUMBER  # NumberExpr
       | BOOLEAN # BooleanExpr
       | STRING  # StringExpr
       | ID      # IdentifierExpr 
       ;

functionDef: '(' ID parameters ')' expr; // Name of the function, parameters, and function body

parameters: ID*; // List of parameters

condPair: '(' expr expr ')'; // Condition and expression pair

// Arithmetical Operator rules
arOperator: '*' | '/'
          | '+' | '-'
          ;

relOperator: '<' | '>'
           | '<=' | '>='
           | '=' | '<>'
           ;

letBinding: '(' ID expr ')'; // Variable name and its value

NUMBER: [0-9]+ ('.' [0-9]+)?;
BOOLEAN: '#t' | '#f'; 
STRING: '"' .*? '"'; // Matches strings in double quotes
ID: [a-zA-Z_][a-zA-Z0-9_\-]*;

COMMENT: ';' ~[\r\n]* -> skip; // Matches comments starting with ';' and skips them
WS: [ \t\r\n]+ -> skip; // Skip whitespace