from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import time


class SessionExpiryMiddleware(MiddlewareMixin):
    """
    Middleware для проверки истечения сессии и автоматического редиректа на главную страницу.

    Работает следующим образом:
    1. При первом входе пользователя сохраняет время создания сессии
    2. При каждом запросе проверяет, не истекла ли сессия
    3. Если сессия истекла - выполняет logout и редирект на главную
    4. Если SESSION_SAVE_EVERY_REQUEST = True, то время обновляется (скользящее окно)
    5. Если SESSION_SAVE_EVERY_REQUEST = False, то время фиксировано (абсолютное истечение)

    Диаграмма работы:

    Запрос → Пользователь аутентифицирован?
              ├─ Нет → Пропустить middleware
              └─ Да → Это страница login/logout?
                       ├─ Да → Пропустить middleware
                       └─ Нет → Есть last_activity в сессии?
                                 ├─ Нет → Сохранить текущее время → Продолжить
                                 └─ Да → (Текущее время - last_activity) > SESSION_COOKIE_AGE?
                                          ├─ Да → Logout → Редирект на главную
                                          └─ Нет → Обновить last_activity → Продолжить
    """

    def process_request(self, request):    # ?
        # Пропускаем для неаутентифицированных пользователей
        if not request.user.is_authenticated:
            return None

        # Пропускаем для страниц logout и login, чтобы избежать циклических редиректов
        current_path = request.path
        try:
            login_url = reverse(settings.LOGIN_URL) if hasattr(settings, 'LOGIN_URL') else '/login/'
            logout_url = reverse(settings.LOGOUT_REDIRECT_URL)
        except:
            login_url = '/login/'
            logout_url = '/logout/'

        if current_path in [login_url, logout_url]:
            return None

        # Получаем текущее время
        current_time = time.time()

        # Получаем время последней активности из сессии
        last_activity = request.session.get('last_activity')

        # Если это первый запрос после логина, сохраняем время
        if last_activity is None:
            request.session['last_activity'] = current_time
            request.session['session_created_at'] = current_time
            return None

        # Вычисляем максимальное время жизни сессии
        session_cookie_age = getattr(settings, 'SESSION_COOKIE_AGE', 1209600)  # По умолчанию 2 недели

        # Проверяем, истекла ли сессия
        time_since_last_activity = current_time - last_activity

        if time_since_last_activity > session_cookie_age:
            # Сессия истекла - выполняем logout
            logout(request)

            # Редиректим на главную страницу или LOGOUT_REDIRECT_URL
            redirect_url = getattr(settings, 'LOGOUT_REDIRECT_URL', 'home')

            # Если redirect_url - это имя URL, преобразуем в путь
            try:
                redirect_path = reverse(redirect_url)
            except:
                redirect_path = redirect_url if redirect_url.startswith('/') else f'/{redirect_url}'

            return redirect(redirect_path)

        # Обновляем время последней активности
        # Это создает "скользящее окно" - сессия продлевается при каждом запросе
        request.session['last_activity'] = current_time

        return None
