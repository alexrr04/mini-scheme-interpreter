// MiniScheme grammar
grammar scheme;

root: expr*;

expr: '(' 'define' definition ')'               # DefinitionExpr
    | '(' ID expr* ')'                          # FunctionCallExpr      
    | '(' 'if' expr ifBranch ifBranch? ')'      # IfExpr
    | '(' 'cond' condPair+ elseBranch? ')'      # CondExpr
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

ifBranch: '(' 'begin' expr+ ')'                 # IfBeginExpr
        | expr                                  # IfSingleExpr
        ;              

condPair: '(' expr expr+ ')';                       // (condition expression)

elseBranch: '(' 'else' expr+ ')'                    // (else expression)     
          ;

parameters: ID*;                                    // Zero or more parameters

letBinding: '(' ID expr ')';                        // (variable_name expression)

arOperator: ('*' | '/' | 'mod')                     // Arithmetic operators
          | ('+' | '-')           
          ;

relOperator: '=' | '<>' | '<' | '>' | '<=' | '>='   // Relational operators
           ;

literal: quotedList                             # QuotedListExpr
       | NUMBER                                 # NumberExpr
       | BOOLEAN                                # BooleanExpr
       | STRING                                 # StringExpr
       | ID                                     # IdentifierExpr
       ;

quotedList: '\'' '(' literal* ')'                   // Quoted list
          ;            

NUMBER: '-'? [0-9]+ ('.' [0-9]+)?;                  // Matches numbers: integers and floating point numbers
BOOLEAN: '#t' | '#f';                               // Boolean values: #t or #f
STRING: '"' .*? '"';                                // Matches strings in double quotes
ID: [a-zA-Z_][a-zA-Z0-9_\-]*;                       // Matches identifiers: letters, digits, underscores, and hyphens

COMMENT: ';' ~[\r\n]* -> skip;                      // Matches comments starting with ';' and skips them
WS: [ \t\r\n]+ -> skip;                             // Skip whitespace
LEXICAL_ERROR: . ;                                  // Catch-all rule for lexical errors