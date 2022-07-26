

def get_field_from_expression(expression: str) -> str:
    for i in expression:
        if i in {".", "[", "!", ":"}:
            return expression.split(i, 1)[0]

    return expression
