(define (displayUserInput input)
    (display input)
)

(define (main)
    (display "Enter an input: ")
    (let ((x (read)))
        (displayUserInput x)
    )
)
