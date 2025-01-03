(define (fib n)
    (if (= n 0)
        0
        (if (= n 1)
            1
            (+ (fib (- n 1)) (fib (- n 2)))
        )
    )
)

(define (helper i n)
    (if (< i n)
        (begin
            (display (fib i))
            (if (< (+ i 1) n)
                (display " "))
            (helper (+ i 1) n)
        )
    )
)

(define (print-fib-series n)
    (helper 0 n)
)

(define (main)
    (display "Enter the number of Fibonacci terms to display: ")
    (define n (read))
    (newline)
    (display "The Fibonacci series is: ")
    (print-fib-series n)
    (newline)
)
