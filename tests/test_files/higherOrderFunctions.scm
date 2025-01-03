;; This file contains a set of higher-order functions and their usage examples.
;;
;; Functions:
;; - apply-twice: Applies a given function twice to an argument.
;; - add1: Increments a given number by 1.
;; - doble: Multiplies a given number by 2.
;; - triple: Multiplies a given number by 3.
;; - parell: Checks if a given number is even.
;; - main: Demonstrates the usage of the above functions by:
;;   - Applying `add1` twice to the number 5 and displaying the result.
;;   - Creating a list `lst` and displaying the result of mapping `doble` over it.
;;   - Displaying the result of filtering even numbers from `lst`.
;;   - Displaying the result of filtering even numbers from the list obtained by mapping `triple` over `lst`.
;;
;; Expected Output:
;; - The result of applying `add1` twice to 5 should be 7.
;; - The list `lst` after mapping `doble` should contain elements doubled.
;; - The filtered list of even numbers from `lst` should contain only even numbers.
;; - The filtered list of even numbers from the list obtained by mapping `triple` over `lst` should contain only even numbers.


(define (apply-twice f x) 
    (f (f x))
)

(define (add1 x)
    (+ x 1)
)

(define (doble x)
    (* x 2)
)

(define (triple x)
    (* x 3)
)

(define (parell x)
    (= (mod x 2) 0)
)

(define (main)
    (display (apply-twice add1 5))
    (newline)
    (define lst '(1 2 3 4))
    (display (map doble lst))
    (newline)
    (display (filter parell lst))
    (newline)
    (display (filter parell (map triple lst)))
)