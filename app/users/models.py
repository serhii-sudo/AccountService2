from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import strip_tags


class CustomUserManager(BaseUserManager):
    # метод для создания обычного пользователя
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The give email must be set')

        # Нормализация email (приведение к нижнему регистру, обработка доменной части)
        email = self.normalize_email(email)

        # Создание объекта пользователя (но еще не сохранение в БД)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        # установка и хеширование пароля
        user.set_password(password)

        # Сохранение пользователя в базу данных
        # using=self._db - использование текущей базы данных (для поддержки мульти-БД)
        user.save(using=self._db)

        # возврат созданного пользователя
        return user

    # Метод для создания суперпользователя (администратора)
    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)  # доступ к админке
        extra_fields.setdefault("is_superuser", True)  # все права

        if extra_fields.get("is_staff") is not True:
            raise ValueError("superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("superuser must have is_superuser=True")

        return self.create_user(email, first_name, last_name, password, **extra_fields)


class CustomUser(AbstractUser):
    COUNTRY_CHOICES = [
        ('', 'Select country'),
        ('US', 'United States, Washington +1 202'),
        ('IQ', 'Iraq, Baghdad +964 1'),
        ('GB', 'United Kingdom, London +44 20'),
        ('DE', 'Germany, Berlin +49 30'),
        ('FR', 'France, Paris +33 1'),
        ('LY', 'Libya, Tripoli +218 21'),
        ('AR', 'Argentina, Buenos Aires +54 11'),
        ('DZ', 'Algeria, Algiers +213 21'),
        ('CI', "Côte d'Ivoire, Abidjan +225 27"),
        ('ZA', 'South Africa, Cape Town +27 21')
    ]


    # Обычно для страны используют max_length=2 (если хранят ISO-коды типа US, RU, GB), потому что выборка идёт по коду, а не по полному названию.
    email = models.EmailField(unique=True, max_length=70)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address1 = models.CharField(max_length=100, blank=True, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True, choices=COUNTRY_CHOICES)
    provinces = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    marketing_consent1 = models.BooleanField(default=False)
    marketing_consent2 = models.BooleanField(default=False)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    # Указание кастомного менеджера пользователей
    objects = CustomUserManager()
    # Указываем, что поле email будет использоваться как идентификатор пользователя (вместо username)
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name", "last_name"]  # поля для бд при регистрации > createsuperuser

    def __str__(self):
        return self.email

    def clean(self):
        for field in [
            "address1",
            "address2",
            "city",
            "country",
            "provinces",
            "postal_code",
            "phone",
        ]:
            value = getattr(self, field)
            if value:
                setattr(self, field, strip_tags(value))



