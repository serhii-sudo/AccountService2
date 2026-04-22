from django import forms


class StripCharFieldMixin:
    """
    Миксин для автоматической установки strip=True для всех полей CharField.
    Требует, чтобы класс формы наследовался от django.forms.Form или его подклассов.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Установка strip=True для всех CharField, fields ожидается от формы
        for field in self.fields.values():  # type: ignore[attr-defined]
            if isinstance(field, forms.CharField) or isinstance(field, forms.EmailField):
                field.strip = True
