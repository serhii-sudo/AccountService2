from datetime import datetime

from django.contrib import messages, auth
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView

from app.settings import LOGOUT_REDIRECT_URL
from users.forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm
from users.models import CustomUser


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_year"] = datetime.now().year
        return context


class CustomRegisterUserView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "register.html"

    def form_valid(self, form):
        user: CustomUser = form.save()
        login(self.request, user)
        messages.success(self.request, "Welkom!")
        return redirect("profile_update")


class CustomLoginUserView(LoginView):
    form_class = CustomUserLoginForm
    template_name = "login.html"


class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserUpdateForm
    template_name = "profile_update.html"
    success_url = reverse_lazy("profile_update")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        # обновляем сессию чтобы не выбросило из аккаунта
        auth.update_session_auth_hash(self.request, self.object)
        messages.success(self.request, "Your profile has been successfully updated!")
        return response

    def post(self, request, *args, **kwargs):
        print(request.POST)  # -> для видимости
        if "delete_profile" in request.POST:
            request.user.delete()
            messages.warning(request, "Your profile has been successfully deleted!")
            return redirect("register")

        return super().post(request, *args, **kwargs)


def logout_view(request):
    logout(request)
    return redirect(LOGOUT_REDIRECT_URL)
