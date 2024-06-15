from form_tui import Field
import unittest


class FieldTest(unittest.TestCase):
    def test_validate(self):
        without_validator = Field("email", "Email", str)
        self.assertTrue(without_validator.validate("string"))
        self.assertTrue(without_validator.validate(""))

        with_validator = Field("email", "Email", str, lambda s: "@" in s)
        self.assertTrue(with_validator.validate("me@email.com"))
        self.assertFalse(with_validator.validate(""))


if __name__ == "__main__":
    unittest.main()
