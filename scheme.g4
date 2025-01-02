// MiniScheme grammar
grammar scheme;

root: expr*;

expr: '(' 'define' definition ')'       # DefinitionExpr
    | '(' ID expr* ')'             # FunctionCallExpr      
    | '(' 'if' expr expr expr ')'   # IfExpr
    | '(' 'cond' condPair+ ')'     # CondExpr
    | '(' 'and' expr+ ')'             # AndExpr
    | '(' 'or' expr+ ')'              # OrExpr
    | '(' 'not' expr ')'              # NotExpr
    | '(' arOperator expr+ ')'       # ArithmeticOperationExpr
    | '(' relOperator expr+ ')'      # RelationalOperationExpr
    | '(' 'car' expr ')'             # CarExpr
    | '(' 'cdr' expr ')'             # CdrExpr
    | '(' 'cons' expr expr ')'       # ConsExpr
    | '(' 'null?' expr ')'           # NullExpr
    | '(' 'let' '(' letBinding+ ')' expr+ ')' # LetExpr
    | '(' 'display' expr ')'         # DisplayExpr
    | '(' 'read' ')'                 # ReadExpr
    | '(' 'newline' ')'              # NewlineExpr
    | literal                        # LiteralExpr
    ;
    // | '(' 'define' functionDef ')'  # FunctionDefinitionExpr  

literal: '\'' '(' literal* ')' # ListExpr
       | NUMBER  # NumberExpr
       | BOOLEAN # BooleanExpr
       | STRING  # StringExpr
       | ID      # IdentifierExpr 
       ;

definition: '(' ID parameters ')' expr* # FunctionDefinitionExpr
          | ID expr  # ConstantDefinitionExpr
          ; 

parameters: ID*; // List of parameters

condPair: '(' expr expr ')'; // Condition and expression pair

// Arithmetic Operator rules
arOperator: '*' | '/' | 'mod'
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