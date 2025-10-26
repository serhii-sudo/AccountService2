from django.urls import path

from users.views import HomePageView, CustomRegisterUserView, CustomLoginUserView, \
    CustomUserUpdateView, logout_view

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('register/', CustomRegisterUserView.as_view(), name='register'),
    path('login/',  CustomLoginUserView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile_update/', CustomUserUpdateView.as_view(), name='profile_update'),

]
