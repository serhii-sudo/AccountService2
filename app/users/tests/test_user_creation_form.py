
from django.test import TestCase


from users.forms import CustomUserCreationForm
from users.forms_constans import ERROR_MESSAGES
from users.models import CustomUser


class TestCustomUserCreationForm(TestCase):
    #  Настройка данных нового пользователя
    def setUp(self):
        self.data = {
            "email": "lampard@gmail.com",
            "first_name": "Frank",
            "last_name": "Lampard",
            "password1": "passlam123@",
            "password2": "passlam123@",
            "marketing_consent1": True,
            "marketing_consent2": True,
        }

    def test_valid_form(self):
        # Создаем форму с данными
        form = CustomUserCreationForm(data=self.data)

        # 1. Проверяем, что форма валидна
        self.assertTrue(form.is_valid(), form.errors)

        # 2. Сохраняем пользователя
        user = form.save()

        # 3. Проверяем, что пользователь создан в базе
        self.assertEqual(user.email, "lampard@gmail.com")
        self.assertEqual(user.first_name, "Frank")
        self.assertEqual(user.last_name, "Lampard")

        # 5. Проверяем чекбоксы маркетинговых согласий
        self.assertTrue(user.marketing_consent1)
        self.assertTrue(user.marketing_consent2)

        # 4. Проверяем, что пароль установлен корректно
        self.assertTrue(user.check_password("passlam123@"))


    def test_strip_whitespace(self):
        data = self.data.copy()
        data.update(
            {
                "email": " Lampard@gmail.com    ",     # проверка на пробелы и регистр
                "first_name": " Frank           ",
                "last_name": " Lampard    ",
                "password1": "  passlam123@  ",
                "password2": " passlam123@   "
            }
        )
        form = CustomUserCreationForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['email'], 'lampard@gmail.com')
        self.assertEqual(form.cleaned_data['first_name'], 'Frank')
        self.assertEqual(form.cleaned_data['last_name'], 'Lampard')
        self.assertEqual(form.cleaned_data['password1'], 'passlam123@')
        self.assertEqual(form.cleaned_data['password2'], 'passlam123@')


    def test_if_email_is_empty(self):
        data = self.data.copy()
        form = CustomUserCreationForm(data=data)
        data.update(
            {
                "email": " ",             # проверяем на пустой email, first_name, last_name
                "first_name": " ",
                "last_name": " "
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn(ERROR_MESSAGES["email"]["required"], form["email"].errors)
        self.assertIn(ERROR_MESSAGES["first_name"]["required"], form["first_name"].errors)
        self.assertIn(ERROR_MESSAGES["last_name"]["required"], form["last_name"].errors)



    def test_if_first_name_is_too_long(self):
        data = self.data.copy()
        form = CustomUserCreationForm(data=data)
        data.update(
            {
                "first_name": 'Name' * 13   # проверяем на слишком длинное имя, то есть умножаем 4 символа на 13
            }
        )
        self.assertTrue(not form.is_valid())
        self.assertIn(ERROR_MESSAGES["first_name"]["max_length"],form["first_name"].errors)
        # print(form["first_name"].errors)
