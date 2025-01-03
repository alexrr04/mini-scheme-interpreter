(define (even x)
    (= (mod x 2) 0))

(define (collatz x)
    (cond ((= x 1) 1)
          ((even x) (collatz (/ x 2)))
          (#t (collatz (+ (* 3 x) 1)))))

(define (main)
    (display "Enter a number and apply the Collatz Conjecture: ")
    (define x (read))
    (newline)
    (display "You entered: ")
    (display x)
    (newline)
    (display "Applying the Collatz Conjecture returns: ")
    (display (collatz x)))


