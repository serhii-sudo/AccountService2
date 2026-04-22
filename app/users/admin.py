from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser  # можно указать, по желанию

    list_display = (
        "colored_email",
        "first_name",
        "last_name",
        "country",
        "phone",
        "date_joined",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("email", "first_name", "username", "phone")  # подключение строки поиска по заданным полям
    ordering = ("-date_joined",)  # сортирование пользователей по дате, самые новые сверху списка
    empty_value_display = "Unknown"  # вместо обычного - будет значение Unknown

    @admin.display()
    def colored_email(self, obj):
        url = reverse("admin:users_customuser_change", args=[obj.pk])
        return format_html(
            f'<a class="button" style="padding:4px 8px; background:#4CAF50; '
            f'color:white; border-radius:4px;" href="{url}">{obj.email}</a>'
        )  # рабочий подход, но устаревший стиль

    # format_html - безопасный способ вставки HTML в admin,
    # проверяет HTML и автоматически экранирует любые опасные символы в подставленных значениях.

    colored_email.short_description = "Email"  # метод, который возвращает HTML с нужным цветом

    list_display_links = ("colored_email",)  # указывает, по какому полю кликаем для редактирования
