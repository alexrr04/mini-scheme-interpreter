(define (main)
    (define lst '(1 2 3 4))
    (display (car lst)) ; 1
    (newline)
    (display (cdr lst)) ; (2 3 4)
    (newline)
    (display (cons 0 lst)) ; (0 1 2 3 4)
    (newline)
    (display (null? lst)) ; #f
    (newline)
    (display (null? '())) ; #t
    (newline)
)
