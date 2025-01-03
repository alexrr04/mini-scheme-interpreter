;; This test file is designed to test the behavior of `let` bindings in a Scheme interpreter.
;; It checks the following:
;; 
;; 1. The correct evaluation of expressions within a `let` binding:
;;    - The first `let` binding defines `x` as 10 and `y` as 5, and displays the result of `(+ x y)`, which should be 15.
;;    - The second `let` binding defines `a` as 7 and `b` as 3, and displays the result of `(* a b)`, which should be 21.
;; 
;; 2. The scope of variables defined within `let` bindings:
;;    - After the `let` bindings, an attempt to display `x` should result in an error because `x` is not defined in the global scope.
;; 
;; 3. The interpreter's handling of errors:
;;    - The display of `23` should not be printed because the previous line causes an error due to the undefined variable `x`.
;; 
;; Expected Output:
;; 15
;; 21
;; Error: Undefined variable x


(define (main)
    (newline)
    (let ((x 10) (y 5))
        (display (+ x y)) ; 15
        (newline))
    (let ((a 7) (b 3))
        (display (* a b))) ; 21
    (newline)
    (display x) ; Error: Undefined variable x
    (display 23) ; This should not be printed
)
