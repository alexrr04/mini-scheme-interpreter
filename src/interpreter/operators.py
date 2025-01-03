ARITHMETIC_OPERATIONS = {
    "+": lambda acc, y: acc + y,
    "-": lambda acc, y: acc - y,
    "*": lambda acc, y: acc * y,
    "/": lambda acc, y: acc // y,
    "mod": lambda acc, y: acc % y,
}

RELATIONAL_OPERATIONS = {
    "<": lambda x, y: x < y,
    ">": lambda x, y: x > y,
    "<=": lambda x, y: x <= y,
    ">=": lambda x, y: x >= y,
    "=": lambda x, y: x == y,
    "<>": lambda x, y: x != y,
}