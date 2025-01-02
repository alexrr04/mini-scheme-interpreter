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

(define (parell x)
    (= (modulo x 2) 0)
)

(define (filter predicat llista)
    (cond
        ((null? llista) '())  ;
        ((predicat (car llista))
            (cons (car llista) (filter predicat (cdr llista))))
        (#t (filter predicat (cdr llista)))
    )
)

(define (main)
    (display (aply-twice add1 5))
    (newline)
    (display (map doble '(1 2 3 4)))
    (newline)
    (display (filter parell '(1 2 3 4)))
)