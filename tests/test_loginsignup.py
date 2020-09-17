import unittest
from contextlib import contextmanager

import loginsignup


@contextmanager
def mockInput(mock):
    original_input = __builtins__.input
    __builtins__.input = lambda _: mock
    yield
    __builtins__.input = original_input


class TestSignup(unittest.TestCase):

    def test_signup_email_valid(self):
        cl = loginsignup.Signup()
        with mockInput("morganzwest@gmail.com"):
            cl.signup_email(tests = True)
            self.assertEqual(cl.i, 4)

    def test_signup_email_invalid_Empty(self):
        cl = loginsignup.Signup()
        with mockInput(""):
            with self.assertRaises(ValueError):
                cl.signup_email(tests = True)
            self.assertEqual(cl.i, 0)

    def test_signup_email_invalid_notAtSYMBOL(self):
        cl = loginsignup.Signup()
        with mockInput("username"):
            with self.assertRaises(ValueError):
                cl.signup_email(tests = True)
            self.assertEqual(cl.i, 2)

    def test_signup_email_invalid_NoDomain(self):
        cl = loginsignup.Signup()
        with mockInput("username@"):
            with self.assertRaises(ValueError):
                cl.signup_email(tests = True)
            self.assertEqual(cl.i, 3)

    def test_signup_email_invalid_NoDOT(self):
        cl = loginsignup.Signup()
        with mockInput("username@domain"):
            with self.assertRaises(ValueError):
                cl.signup_email(tests = True)
            self.assertEqual(cl.i, 3)

    def test_signup_email_invalid_EndsWithDOT(self):
        cl = loginsignup.Signup()
        with mockInput("username@domain."):
            with self.assertRaises(ValueError):
                cl.signup_email(tests = True)
            self.assertEqual(cl.i, 3)

    def test_signup_email_invalid_alreadyUsed(self):
        cl = loginsignup.Signup()
        with mockInput("testholdemail@gmail.com"):
            with self.assertRaises(ValueError):
                cl.signup_email(tests = True)

    def test_signup_username_valid(self):
        cl = loginsignup.Signup()
        with mockInput("username"):
            cl.signup_username()
            self.assertGreater(len(cl.username), 0)

    def test_signup_username_invalid_Empty(self):
        cl = loginsignup.Signup()
        with mockInput(""):
            with self.assertRaises(ValueError):
                cl.signup_username(tests = True)

    def test_signup_password_valid(self):
        cl = loginsignup.Signup()
        with mockInput("A1dfgt"):
            cl.signup_password(tests = True)
            self.assertTrue(cl.valid)

    def test_signup_password_invalid_EmptyString(self):
        cl = loginsignup.Signup()
        with mockInput(""):
            with self.assertRaises(ValueError):
                cl.signup_password(tests = True)

    def test_signup_password_invalid_DigitOnly(self):
        cl = loginsignup.Signup()
        with mockInput("1"):
            with self.assertRaises(ValueError):
                cl.signup_password(tests = True)

    def test_signup_password_invalid_CapitalOnly(self):
        cl = loginsignup.Signup()
        with mockInput("C"):
            with self.assertRaises(ValueError):
                cl.signup_password(tests = True)

    def test_signup_password_invalid_LowerOnly(self):
        cl = loginsignup.Signup()
        with mockInput("a"):
            with self.assertRaises(ValueError):
                cl.signup_password(tests = True)

    def test_signup_password_invalid_1(self):
        cl = loginsignup.Signup()
        with mockInput("abc1"):
            with self.assertRaises(ValueError):
                cl.signup_password(tests = True)

    def test_signup_password_invalid_2(self):
        cl = loginsignup.Signup()
        with mockInput("Abc5"):
            with self.assertRaises(ValueError):
                cl.signup_password(tests = True)

    def test_signup_password_invalid_3(self):
        cl = loginsignup.Signup()
        with mockInput("Abc1G"):
            with self.assertRaises(ValueError):
                cl.signup_password(tests = True)

    def test_signup_ipbanned_banned(self):
        cl = loginsignup.Signup()
        cl.signup_checks("*")
        self.assertTrue(cl.banned)

    def test_signup_ipbanned_unbanned(self):
        cl = loginsignup.Signup()
        cl.signup_checks("")
        self.assertFalse(cl.banned, msg = "Current IP is resulting banned.")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSignup)
    unittest.TextTestRunner(verbosity = 2).run(suite)

