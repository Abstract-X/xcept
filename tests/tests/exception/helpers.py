import pytest


pytest_message_parametrize = pytest.mark.parametrize(
    ("template", "test_field_value", "expected_result"),
    (
        # Empty message
        ("", None, ""),

        # Test field type «int»
        ("message", 12345, "message"),
        ("{test_field}", 12345, "12345"),
        ("{test_field!s}", 12345, "12345"),
        ("{test_field!r}", 12345, "12345"),
        ("{test_field!a}", 12345, "12345"),
        ("{test_field:<10}", 12345, "12345     "),
        ("{test_field:>10}", 12345, "     12345"),
        ("{test_field:0=10}", 12345, "0000012345"),
        ("{test_field:0^10}", 1234, "0001234000"),
        ("{test_field:+}", 12345, "+12345"),
        ("{test_field:+}", -12345, "-12345"),
        ("{test_field:-}", 12345, "12345"),
        ("{test_field:-}", -12345, "-12345"),
        ("{test_field: }", 12345, " 12345"),
        ("{test_field: }", -12345, "-12345"),
        ("{test_field:b}", 12345, "11000000111001"),
        ("{test_field:c}", 100, "d"),
        ("{test_field:d}", 12345, "12345"),
        ("{test_field:o}", 12345, "30071"),
        ("{test_field:x}", 1234, "4d2"),
        ("{test_field:X}", 1234, "4D2"),
        ("{test_field:.2%}", 1, "100.00%"),
        ("{test_field:}", 12345, "12345"),
        ("{test_field:,}", 123456789, "123,456,789"),

        # Test field type «float»
        ("message", 123.45, "message"),
        ("{test_field!s}", 123.45, "123.45"),
        ("{test_field!r}", 123.45, "123.45"),
        ("{test_field!a}", 123.45, "123.45"),
        ("{test_field:<10}", 123.45, "123.45    "),
        ("{test_field:>10}", 123.45, "    123.45"),
        ("{test_field:0=10}", 123.45, "0000123.45"),
        ("{test_field:0^10}", 1.23, "0001.23000"),
        ("{test_field:+}", 123.45, "+123.45"),
        ("{test_field:+}", -123.45, "-123.45"),
        ("{test_field:-}", 123.45, "123.45"),
        ("{test_field:-}", -123.45, "-123.45"),
        ("{test_field: }", 123.45, " 123.45"),
        ("{test_field: }", -123.45, "-123.45"),
        ("{test_field:e}", 123.45, "1.234500e+02"),
        ("{test_field:E}", 123.45, "1.234500E+02"),
        ("{test_field:f}", 123.45, "123.450000"),
        ("{test_field:f}", float("nan"), "nan"),
        ("{test_field:f}", float("inf"), "inf"),
        ("{test_field:F}", float("nan"), "NAN"),
        ("{test_field:F}", float("inf"), "INF"),
        ("{test_field:g}", 123.4567, "123.457"),
        ("{test_field:G}", 123.4567, "123.457"),
        ("{test_field:.2%}", 0.5, "50.00%"),
        ("{test_field:}", 123.45, "123.45"),

        # Test field type «str»
        ("message", "foo", "message"),
        ("{test_field}", "foo", "foo"),
        ("{test_field!s}", "foo", "foo"),
        ("{test_field!r}", "foo", "'foo'"),
        ("{test_field!a}", "foo", "'foo'"),
        ("{test_field:<10}", "foo", "foo       "),
        ("{test_field:>10}", "foo", "       foo"),
        ("{test_field:0^10}", "foo", "000foo0000"),
        ("{test_field:s}", "foo", "foo"),
        ("{test_field:}", "foo", "foo"),

        # Test field with index
        ("{test_field[0]}", [100, 200, 300], "100"),

        # Test field with attribute
        ("{test_field.real}", 123.45, "123.45"),

        # Multiple replacement
        ("{test_field} {test_field[0].real}", [123.45], "[123.45] 123.45"),

        # Unknown field
        ("{test_field} {unknown_field}", "foo", "foo <UNKNOWN>"),
        ("{test_field!s} {unknown_field!s}", "foo", "foo <UNKNOWN>"),
        ("{test_field!r} {unknown_field!r}", "foo", "'foo' <UNKNOWN>"),
        ("{test_field!a} {unknown_field!a}", "foo", "'foo' <UNKNOWN>"),
        ("{test_field} {}", "foo", "foo <UNKNOWN>"),
        ("{test_field!s} {!s}", "foo", "foo <UNKNOWN>"),
        ("{test_field!r} {!r}", "foo", "'foo' <UNKNOWN>"),
        ("{test_field!a} {!a}", "foo", "'foo' <UNKNOWN>"),
        ("{test_field} {0}", "foo", "foo <UNKNOWN>"),
        ("{test_field!s} {0!s}", "foo", "foo <UNKNOWN>"),
        ("{test_field!r} {0!r}", "foo", "'foo' <UNKNOWN>"),
        ("{test_field!a} {0!a}", "foo", "'foo' <UNKNOWN>"),

        # Equal sign expression
        ("{test_field=}", 12345, "test_field=12345"),
        ("{test_field=}", 123.45, "test_field=123.45"),
        ("{test_field=}", "foo", "test_field='foo'"),
        ("{test_field=} {unknown_field=}", "foo", "test_field='foo' unknown_field=<UNKNOWN>"),

        # Several unknown fields in a row
        (
            "{unknown_field_1} {unknown_field_2} {test_field}",
            "foo",
            "<UNKNOWN> <UNKNOWN> foo"
        ),
        (
            "{unknown_field_1!s} {unknown_field_2!r} {unknown_field_3!a} {test_field}",
            "foo",
            "<UNKNOWN> <UNKNOWN> <UNKNOWN> foo"
        ),
        (
            "{unknown_field_1=} {unknown_field_2=} {test_field=}",
            "foo",
            "unknown_field_1=<UNKNOWN> unknown_field_2=<UNKNOWN> test_field='foo'"
        ),
        (
            "{test_field} {unknown_field_1} {unknown_field_2}",
            "foo",
            "foo <UNKNOWN> <UNKNOWN>"
        ),
        (
            "{test_field} {unknown_field_1!s} {unknown_field_2!r} {unknown_field_3!a}",
            "foo",
            "foo <UNKNOWN> <UNKNOWN> <UNKNOWN>"
        ),
        (
            "{test_field=} {unknown_field_1=} {unknown_field_2=}",
            "foo",
            "test_field='foo' unknown_field_1=<UNKNOWN> unknown_field_2=<UNKNOWN>"
        )
    )
)
