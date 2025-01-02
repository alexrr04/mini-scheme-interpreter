(define (aply-twice f x) 
    (f (f x))
)

(define (add1 x)
    (+ x 1)
)

(define (doble x)
    (* x 2)
)

(define (map func llista)
    (cond
        ((null? llista) '())
        (#t (cons (func (car llista)) (map func (cdr llista))))
    )
)

(define (main)
    (display (aply-twice add1 5))
    (newline)
    (display (map doble '(1 2 3 4)))
)