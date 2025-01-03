;; This test file contains a series of operations to test the functionality of the mini-scheme interpreter.
;; It tests basic arithmetic operations, comparison operations, and equality checks.
;;
;; The operations tested are:
;; - Addition: (+ 3 5) should output 8
;; - Subtraction: (- 10 7) should output 3
;; - Multiplication: (* 6 7) should output 42
;; - Division: (/ 20 4) should output 5
;; - Modulus: (mod 10 3) should output 1
;; - Less than: (< 5 10) should output #t (true)
;; - Less than: (< 10 5) should output #f (false)
;; - Greater than or equal to: (>= 10 10) should output #t (true)
;; - Equality: (= 4 4) should output #t (true)
;; - Not equal: (<> 4 4) should output #f (false)
;;
;;
;; Expected Output:
;; 8
;; 3
;; 42
;; 5
;; 1
;; #t
;; #f
;; #t
;; #t
;; #f


(define (main)
    (display (+ 3 5))
    (newline)
    (display (- 10 7))
    (newline)
    (display (* 6 7))
    (newline)
    (display (/ 20 4))
    (newline)
    (display (mod 10 3))
    (newline)
    (display (< 5 10))
    (newline)
    (display (< 10 5))
    (newline)
    (display (>= 10 10))
    (newline)
    (display (= 4 4))
    (newline)
    (display (<> 4 4))
    (newline)
)