from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView

from app.settings import LOGOUT_REDIRECT_URL
from users.forms import CustomUserCreationForm, CustomUserLoginForm, CustomUserUpdateForm


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_year'] = datetime.now().year
        return context


class CustomRegisterUserView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('profile_update')


class CustomLoginUserView(LoginView):
    form_class = CustomUserLoginForm
    template_name = 'login.html'


class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CustomUserUpdateForm
    template_name = 'profile_update.html'
    success_url = reverse_lazy('profile_update')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been successfully updated!')
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if "delete_profile" in request.POST:
            user = request.user
            user.delete()
            messages.success(request, 'Your profile has been successfully deleted!')
            return redirect("register")
        return super().post(request, *args, **kwargs)


def logout_view(request):
    logout(request)
    return redirect(LOGOUT_REDIRECT_URL)
