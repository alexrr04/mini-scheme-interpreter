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
    (= (mod x 2) 0)
)

(define (main)
    (define lst '(1 2 3 4))
    (display (aply-twice add1 5))
    (newline)
    (display (map doble lst))
    (newline)
    (display (filter parell lst))
)