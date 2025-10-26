from django.contrib.auth import get_user_model
from django.test import TestCase

from users.forms import CustomUserUpdateForm



class TestUserUpdateForm(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_user(  # type: ignore - разобрать
            email="lampard@gmail.com",
            first_name="Frank",
            last_name="Lampard",
            password="passlam123@"
        )

    def test_change_password(self):
        # данные для обновления
        data = {
            "email": "lampard@gmail.com",
            "first_name": "Frank",
            "last_name": "Lampard",
            "password": "frenkie_fix1978"
        }

        # форма получает существующий объект через instance
        form = CustomUserUpdateForm(data=data, instance=self.user)
        self.assertTrue(form.is_valid(), form.errors)

        form.save()
        self.user.refresh_from_db()

        self.assertFalse(self.user.check_password('passlam123@'))
        self.assertTrue(self.user.check_password('frenkie_fix1978'))















