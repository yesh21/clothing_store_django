from django.urls import path
from . import views

app_name = "login"

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("signup/", views.RegisterView.as_view(), name="signup"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("reset-password/", views.ResetPasswordView.as_view(), name="passwordReset"),
    path("profile/", views.profile, name="users-profile"),
    path("forgot/", views.ChangePasswordView.as_view()),
]
