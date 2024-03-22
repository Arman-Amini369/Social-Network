from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from home.models import Post

class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = "account/user_register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        context = {
            "form" : form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):   
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd["username"], cd["email"], cd["password1"])
            messages.success(request, "You Registered Successfully", "success")
            return redirect("account:user_login")
        context = {
            "form" : form,
        }
        return render(request, self.template_name, context)


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = "account/user_login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        context = {
            "form" : form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd["password"])
            if user is not None:
                login(request, user)
                messages.success(request, "You Logged In Successfully", "success")
                return redirect("home:home")
            else:
                messages.error(request, "Wrong Username or Password", "danger")
                return redirect("account:user_login")
        
        context = {
            "form" : form,
        }

        return render(request, self.template_name, context)


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "You Logged Out Successfully", "success")
        return redirect("home:home")


class UserProfileVIew(View):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        posts = Post.objects.filter(user=user)
        context = {
            "user" : user,
            "posts" : posts,
        }
        return render(request, "account/user_profile.html", context)


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = "account/password_reset_form.html"
    success_url = reverse_lazy("account:password_reset_done")
    email_template_name = "account/password_reset_email.html"