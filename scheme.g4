// MiniScheme grammar
grammar scheme;

root: expr*;

expr: '(' 'define' definition ')'               # DefinitionExpr
    | '(' ID expr* ')'                          # FunctionCallExpr      
    | '(' 'if' expr expr expr ')'               # IfExpr
    | '(' 'cond' condPair+ ')'                  # CondExpr
    | '(' 'and' expr+ ')'                       # AndExpr
    | '(' 'or' expr+ ')'                        # OrExpr
    | '(' 'not' expr ')'                        # NotExpr
    | '(' arOperator expr+ ')'                  # ArithmeticOperationExpr
    | '(' relOperator expr+ ')'                 # RelationalOperationExpr
    | '(' 'car' expr ')'                        # CarExpr
    | '(' 'cdr' expr ')'                        # CdrExpr
    | '(' 'cons' expr expr ')'                  # ConsExpr
    | '(' 'null?' expr ')'                      # NullExpr
    | '(' 'let' '(' letBinding+ ')' expr+ ')'   # LetExpr
    | '(' 'display' expr ')'                    # DisplayExpr
    | '(' 'read' ')'                            # ReadExpr
    | '(' 'newline' ')'                         # NewlineExpr
    | literal                                   # LiteralExpr
    ;

definition: '(' ID parameters ')' expr*         # FunctionDefinitionExpr
          | ID expr                             # ConstantDefinitionExpr
          ; 

literal: quotedList                             # QuotedListExpr
       | NUMBER                                 # NumberExpr
       | BOOLEAN                                # BooleanExpr
       | STRING                                 # StringExpr
       | ID                                     # IdentifierExpr
       ;

parameters: ID*;                                    // Zero or more parameters

condPair: '(' expr expr ')';                        // (condition expression)

letBinding: '(' ID expr ')';                        // (variable_name expression)

// Arithmetic Operator rules
arOperator: '*' | '/' | 'mod' | '+' | '-'           // Arithmetic operators
          ;

relOperator: '<' | '>' | '<=' | '>=' | '=' | '<>'   // Relational operators
           ;

quotedList: '\'' '(' literal* ')'                   // Quoted list
          ;            

NUMBER: [0-9]+ ('.' [0-9]+)?;                       // Matches numbers
BOOLEAN: '#t' | '#f';                               // Boolean values: #t or #f
STRING: '"' .*? '"';                                // Matches strings in double quotes
ID: [a-zA-Z_][a-zA-Z0-9_\-]*;

COMMENT: ';' ~[\r\n]* -> skip;                      // Matches comments starting with ';' and skips them
WS: [ \t\r\n]+ -> skip;                             // Skip whitespace