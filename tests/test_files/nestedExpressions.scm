(define (square x) (* x x))

(define (main)
    (define x (read))
    (display x)
    (newline)
    (display (square (+ 2 3))) ; 25
    (newline)
    (display (if (null? '(1 2 3))
                "Empty"
                (cons (square 2) x))) ; (4 4 9)
    (newline)
)
