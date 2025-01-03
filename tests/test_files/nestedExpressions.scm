(define (square x) (* x x))

(define (main)
    (define x (read))
    (display x)
    (newline)
    (display (square (+ 2 3))) ; 25
    (newline)
    (display (if (not (null? '(1 2 3)))
                (cons (square 2) x))) ; (4 4 9)
    (newline)
    (display (cond
                ((null? x) '())
                ((= x 1) '(1))
                (else '(2 3 4)))) ; (2 3 4)
    (newline)
)
