(define (main)
    (newline)
    (let ((x 10) (y 5))
        (display (+ x y)) ; 15
        (newline))
    (let ((a 7) (b 3))
        (display (* a b))) ; 21
    (newline)
    (display x) ; Error: Undefined variable x
    (display 23) ; This should not be printed
)
