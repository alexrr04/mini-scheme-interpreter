def define_builtins():
    """
    Define and return built-in functions for the Mini Scheme interpreter.

    This function provides the definitions for `map` and `filter` as Scheme-like
    expressions. These definitions are returned as a dictionary where the keys 
    are the function names (`map` and `filter`) and the values are tuples containing 
    the parameters and the function body as a string.

    Returns:
        dict: A dictionary mapping built-in function names (`map` and `filter`) 
        to their parameter lists and body strings.
    """
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
        (else (filter f (cdr lst)))
    )
    """

    return {
        'map': (params, map_body_string),
        'filter': (params, filter_body_string),
    }