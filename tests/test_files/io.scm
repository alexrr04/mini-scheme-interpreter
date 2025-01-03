;; This test file contains a mini Scheme program that tests the implementation of the Collatz Conjecture.
;; 
;; Functions:
;; - (even x): Checks if a number x is even.
;; - (collatz x): Applies the Collatz Conjecture to a number x. If x is 1, it returns 1. If x is even, it recursively calls itself with x divided by 2. If x is odd, it recursively calls itself with 3x + 1.
;; - (main): Prompts the user to enter a number, reads the input, and displays the result of applying the Collatz Conjecture to the entered number.
;;
;; Expected Output:
;; - The program will prompt the user to enter a number, display the entered number, and then display the result of the Collatz Conjecture applied to that number.


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


