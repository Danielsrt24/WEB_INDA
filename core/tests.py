from django.test import SimpleTestCase

from core.validation import parse_decimal_at_least, parse_integer_at_least


class NumericValidationTests(SimpleTestCase):
    def test_integer_validation_rejects_negative_values(self):
        with self.assertRaises(ValueError):
            parse_integer_at_least("-1", "Créditos")

        self.assertEqual(parse_integer_at_least("0", "Créditos"), 0)
        self.assertEqual(
            parse_integer_at_least("7", "Distribución", minimum=1),
            7,
        )

    def test_decimal_validation_rejects_negative_and_non_finite_values(self):
        for value in ("-0.01", "NaN", "Infinity"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                parse_decimal_at_least(value, "Calificación", maximum=10)

        self.assertEqual(
            parse_decimal_at_least("0", "Calificación", maximum=10),
            0,
        )
        self.assertEqual(
            parse_decimal_at_least("9.5", "Calificación", maximum=10),
            9.5,
        )

