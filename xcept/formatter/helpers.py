from typing import Optional, Tuple


def get_field_from_expression(expression: str) -> Tuple[str, Optional[str]]:
    for i in expression:
        if i in {".", "[", "!", ":"}:
            return expression.split(i, 1)[0], i

    field = _get_field_from_equal_sign_expression(expression)

    if field is not None:
        return field, "="

    return expression, None


def _get_field_from_equal_sign_expression(expression: str) -> Optional[str]:
    parts = expression.split("=")

    if len(parts) == 2:
        field, remainder = [i.strip(" ") for i in parts]

        if (
            not remainder
            and not field[0].isdigit()
            and all(
                i.isalpha()
                or i.isdigit()
                or i == "_"
                for i in field
            )
        ):
            return field
