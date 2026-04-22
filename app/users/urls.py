from django.urls import path

from users.forms import CustomPasswordResetForm, CustomPasswordResetConfirmForm
from users.views import HomePageView, CustomRegisterUserView, CustomLoginUserView, CustomUserUpdateView, logout_view

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("register/", CustomRegisterUserView.as_view(), name="register"),
    path("login/", CustomLoginUserView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile_update/", CustomUserUpdateView.as_view(), name="profile_update"),
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="password_reset.html",
            form_class=CustomPasswordResetForm,
            email_template_name="password_reset_email.html",
            subject_template_name="password_reset_subject.txt",
            success_url="/password-reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html", form_class=CustomPasswordResetConfirmForm
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
        name="password_reset_complete",
    ),
]
