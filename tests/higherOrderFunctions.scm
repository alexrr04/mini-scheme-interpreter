(define (aply-twice f x) 
    (f (f x))
)

(define (add1 x)
    (+ x 1)
)

(define (doble x)
    (* x 2)
)

(define (parell x)
    (= (modulo x 2) 0)
)

(define (main)
    (display (aply-twice add1 5))
    (newline)
    (display (map doble '(1 2 3 4)))
    (newline)
    (display (filter parell '(1 2 3 4)))
)