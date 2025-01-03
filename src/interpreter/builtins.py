def define_builtins():
    """Returns the built-in function definitions of the interpreter (map and filter)."""
    params = ['f', 'lst']

    # Map function body as a Scheme expression
    map_body_string = """
    (if (null? lst) 
        \'() 
        (cons (f (car lst)) (map f (cdr lst)))
    )
    """

    # Filter function body as a Scheme expression
    filter_body_string = """
    (cond 
        ((null? lst) \'()) 
        ((f (car lst)) (cons (car lst) (filter f (cdr lst))))
        (#t (filter f (cdr lst)))
    )
    """

    return {
        'map': (params, map_body_string),
        'filter': (params, filter_body_string),
    }