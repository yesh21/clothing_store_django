from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
from cart.models import Order

# Create your views here.


def home(request):
    return render(request, "login/html/home.html")


class RegisterView(View):
    form_class = RegisterForm
    initial = {"key": "value"}
    template_name = "login/html/register.html"

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to="/")

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}")

            return redirect(to="/login/")

        return render(request, self.template_name, {"form": form})


# extends builtin loginview
class CustomLoginView(LoginView):
    form_class = LoginForm
    initial = {"key": "value"}
    template_name = "login/html/login.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Successfully logged out")
        return redirect("/login/")


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "login/html/forgot_password.html"
    email_template_name = "login/html/forgot_password.html"
    subject_template_name = "login/password_reset_subject.txt"

    success_message = (
        "We've emailed you instructions for setting your password, "
        "if an account exists with the email you entered. You should receive them shortly."
        " If you don't receive an email, "
        "please make sure you've entered the address you registered with, and check your spam folder."
    )
    success_url = reverse_lazy("login:login")


@login_required
def profile(request):

    orders = Order.objects.filter(user=request.user)
    context = {
        "full_name": request.user.get_full_name(),
        "email": request.user.email,
        "orders": orders,
    }
    return render(request, "login/html/profile.html", context=context)


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = "login/html/profile.html"
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy("login:login")

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user)
        context = {
            "full_name": request.user.get_full_name(),
            "email": request.user.email,
            "orders": orders,
        }
        return render(request, self.template_name, context=context)
