from django.contrib.auth import get_user_model
from django.test import TestCase

from users.forms import CustomUserLoginForm


class CustomUserLoginFormTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.password = "passlam123@"
        self.user = self.User.objects.create_user( # type: ignore - разобрать
            email="lampard@gmail.com",
            first_name="Frank",
            last_name="Lampard",
            password=self.password
        )

    def test_login_form_valid(self):
        form_data = {"username": self.user.email, "password": self.password}
        form = CustomUserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_login_form_invalid_password(self):
        form_data = {"username": self.user.email, "password": "wrongpass"}
        form = CustomUserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("invalid e-mail or password!", form.errors["__all__"])
