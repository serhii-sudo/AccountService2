import bleach
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from users.forms_constans import BASE_WIDGET_ATTRS, ERROR_MESSAGES
from users.mixins import StripCharFieldMixin
from users.models import CustomUser


class CustomUserCreationForm(StripCharFieldMixin, UserCreationForm):
    error_messages = {
        'password_mismatch': 'Passwords do not match',
    }
    # Создание поля email, которое является полем для ввода электронной почты.
    # forms.EmailField — это тип поля формы Django, предназначенный для валидации email-адресов.
    email = forms.EmailField(
        required=True,  # Поле обязательно для заполнения.
        min_length=2,
        max_length=66,  # Максимальная длина email — 66 символов.
        widget=forms.EmailInput(  # Указывает, что для этого поля используется HTML-элемент <input type="email">.
            attrs={  # Атрибуты HTML для поля ввода.
                **BASE_WIDGET_ATTRS,
                'placeholder': 'Your email'
            }
        ),
        error_messages=ERROR_MESSAGES["email"]
    )

    first_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                **BASE_WIDGET_ATTRS,
                "placeholder": "Your first name"
            }
        ),
        error_messages=ERROR_MESSAGES["first_name"]
    )

    last_name = forms.CharField(
        required=True,
        min_length=2,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                **BASE_WIDGET_ATTRS,
                "placeholder": "Your last name"
            }
        ),
        error_messages=ERROR_MESSAGES["last_name"]
    )

    password1 = forms.CharField(
        required=True,
        min_length=2,
        max_length=66,
        widget=forms.PasswordInput(
            attrs={
                **BASE_WIDGET_ATTRS,
                "placeholder": "Password"
            }
        ),
        error_messages=ERROR_MESSAGES["password"]
    )

    password2 = forms.CharField(
        required=True,
        min_length=2,
        max_length=66,
        widget=forms.PasswordInput(
            attrs={
                **BASE_WIDGET_ATTRS,
                "placeholder": "Confirm password"
            }
        ),
        error_messages=ERROR_MESSAGES["password"]

    )
    # Чекбокс согласия на получение маркетинговых рассылок
    # Поле для согласия на получение маркетинговых сообщений.
    # forms.BooleanField — это поле для флажка (checkbox).
    marketing_consent1 = forms.BooleanField(
        required=False,  # Поле необязательное, пользователь может не отмечать флажок.
        label="I agree to receive commercial, promotional, and marketing communications.",
        # Текст метки, отображаемый рядом с флажком.
        widget=forms.CheckboxInput(attrs={"class": "checkbox-input-register"}),
        # Используется HTML-элемент <input type="checkbox"> с CSS-классом "checkbox-input-register".
    )

    # Чекбокс согласия на персонализированные маркетинговые предложения
    # Второе поле для согласия на получение персонализированных маркетинговых сообщений.
    marketing_consent2 = forms.BooleanField(
        required=False,  # Поле необязательное.
        label="I agree to receive personalized commercial communications.",  # Текст метки для флажка.
        widget=forms.CheckboxInput(attrs={"class": "checkbox-input-register"}),
        # Используется HTML-элемент <input type="checkbox"> с тем же CSS-классом.
    )

    # Метаинформация о форме
    class Meta:
        model = CustomUser  # Указывает, с какой моделью работает форма (Django User модель)
        fields = (  # Список полей, которые будут отображены и обработаны формой
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "marketing_consent1",
            "marketing_consent2",
        )

    # Метод валидации email (будет вызван автоматически при вызове form.is_valid())
    def clean_email(self):
        email = self.cleaned_data.get("email").lower()  # Получаем введённый email
        if CustomUser.objects.filter(email=email).exists():  # Проверяем, существует ли пользователь с таким email
            raise forms.ValidationError("This email is already in use.")  # Генерируем ошибку валидации
        return email  # Возвращаем email, если всё корректно

    # Метод сохранения данных формы
    def save(self, commit=True):
        user = super().save(commit=False)  # Создаём объект пользователя, но пока не сохраняем в БД
        user.marketing_consent1 = self.cleaned_data.get("marketing_consent1", True)  # Присваиваем значение из формы
        user.marketing_consent2 = self.cleaned_data.get("marketing_consent2", True)
        if commit:  # Если указано сохранить сразу
            user.save()  # Сохраняем объект в БД
        return user  # Возвращаем объект пользователя


class CustomUserLoginForm(StripCharFieldMixin, AuthenticationForm):
    username = forms.CharField(
        label="Email",
        required=True,
        min_length=2,
        max_length=66,
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                **BASE_WIDGET_ATTRS,
                "placeholder": "Your username"
            }
        ),
        error_messages=ERROR_MESSAGES["username"]
    )

    password = forms.CharField(
        required=True,
        min_length=2,
        max_length=66,
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                **BASE_WIDGET_ATTRS,
                "placeholder": "Your password"
            }
        ),
        error_messages=ERROR_MESSAGES["password"]
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('invalid e-mail or password!')
        return self.cleaned_data


class CustomUserUpdateForm(StripCharFieldMixin, forms.ModelForm):
    email = forms.EmailField(
        required=True,
        min_length=2,
        max_length=66,
        label='Email',
        widget=forms.EmailInput(
            attrs={
                **BASE_WIDGET_ATTRS,
                "placeholder": "your@email.com",
                "autocomplete": "email"
            }
        ),
        error_messages=ERROR_MESSAGES["email"]

    )

    password = forms.CharField(
        required=True,
        min_length=8,
        max_length=66,
        label="New_Password",
        widget=forms.PasswordInput(
            attrs={
                **BASE_WIDGET_ATTRS,
                "placeholder": "Your new_password"
            }
        ),
        error_messages=ERROR_MESSAGES["password"]
    )

    first_name = forms.CharField(
        required=False,
        min_length=2,
        max_length=50,
        label='First name',
        widget=forms.TextInput(
            attrs={
                **BASE_WIDGET_ATTRS,
                "placeholder": "Your first name"
            }
        ),
        error_messages=ERROR_MESSAGES["first_name"]
    )

    last_name = forms.CharField(
        required=False,
        min_length=2,
        max_length=50,
        label="Last name",
        widget=forms.TextInput(
            attrs={
                **BASE_WIDGET_ATTRS,
                "placeholder": "Your last name"
            }
        ),
        error_messages=ERROR_MESSAGES["last_name"]
    )

    phone = forms.CharField(
        required=False,
        label="Phone number",
        validators=[
            RegexValidator(
                r'^\+[1-9]\d+$',  # Международный формат E.164
                message='Enter a valid phone number (e.g. +1234567890...)'
            )
        ],
        widget=forms.TextInput(
            attrs={
                **BASE_WIDGET_ATTRS,
                'placeholder': '+1234567890...',
                'pattern': r'^\+[1-9]\d+$'  # HTML5 валидация
            }
        ),
        error_messages={
            'invalid': 'Enter a valid  phone number'
        },

        help_text="International format with optional '+'"
    )

    postal_code = forms.CharField(
        required=False,
        validators=[
            RegexValidator(
                r'^[A-Za-z\d\-]+$',
                'Enter a valid postal code'
            )
        ],
        widget=forms.TextInput(
            attrs={
                **BASE_WIDGET_ATTRS,
                'placeholder': '12345'
            }
        ),
        error_messages={
            'invalid': 'Enter a valid postal code'
        }
    )

    # Поле для ввода адреса (основная часть, например, улица).
    address1 = forms.CharField(
        required=False,  # Поле необязательное.
        max_length=100,  # Максимальная длина — 100 символов.
        widget=forms.TextInput(attrs={  # HTML-элемент <input type="text">.
            **BASE_WIDGET_ATTRS,  # Распаковка общих атрибутов.
            'placeholder': 'Street address'  # Плейсхолдер с подсказкой.
        })
    )

    # Поле для ввода дополнительной части адреса (например, квартира).
    address2 = forms.CharField(
        required=False,  # Поле необязательное.
        max_length=100,  # Максимальная длина — 100 символов.
        widget=forms.TextInput(
            attrs={
                **BASE_WIDGET_ATTRS,
                'placeholder': 'Apartment, suite, etc.'
            }
        )
    )

    city = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                **BASE_WIDGET_ATTRS,
                'placeholder': 'City'
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'city', 'country',
            'address1', 'address2', 'postal_code', 'phone'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Важно: вызывает миксин + ModelForm

        if not hasattr(CustomUser, 'COUNTRY_CHOICES'):
            raise AttributeError("CustomUser model must define COUNTRY_CHOICES")

            # Для страны и региона лучше использовать select
        self.fields['country'].widget = forms.Select(
            attrs={**BASE_WIDGET_ATTRS},  # 1. Атрибуты HTML-элемента
            choices=[('', 'Select country')] + CustomUser.COUNTRY_CHOICES  # 2. Список выбора
        )


    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            return ''

        world_operators = [
            '+1202', '+9641', '+4420', '+4930', '+331',
            '+21821', '+5411', '+21321', '+22527', '+2721'
        ]
        if not any(phone.startswith(code) for code in world_operators):
            raise ValidationError(
                f" Not correct operator code! {', '.join(world_operators)}"
            )
        return phone


    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is already registered')
        return email


    def clean(self):
        cleaned_data = super().clean()
        for field_name in ['address1', 'address2', 'city']:
            if field_name in cleaned_data:
                cleaned_data[field_name] = bleach.clean(cleaned_data[field_name])
        if cleaned_data.get('address1') and not cleaned_data.get('city'):
            self.add_error('city', 'City is required when providing address')
        return cleaned_data


    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            self.save_m2m()
        return user










