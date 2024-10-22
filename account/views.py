from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from home.models import Post
from .models import Relation


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

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get("next")
        return super().setup(request, *args, **kwargs)

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
                if self.next:
                    return redirect(self.next)
                return redirect("account:user_profile", user.id)
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


class UserProfileVIew(LoginRequiredMixin, View):
    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, pk=user_id)
        posts = user.posts.all()
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            is_following = True
        context = {
            "user" : user,
            "posts" : posts,
            "is_following" : is_following,
        }
        return render(request, "account/user_profile.html", context)


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = "account/password_reset_form.html"
    success_url = reverse_lazy("account:password_reset_done")
    email_template_name = "account/password_reset_email.html"
    

class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "account/password_reset_done.html"


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "account/password_reset_confirm.html"
    success_url = reverse_lazy("account:password_reset_complete")


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = "account/password_reset_complete.html"


class UserFollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            messages.error(request, "You have already followed this user", "danger")
        else:
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request, "You have followed this user", "success")
        return redirect("account:user_profile", user.id)


class UserUnfollowView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, "You have unfollowed this user", "success")
        else:
            messages.error(request, "You have not followed this user", "danger")
        return redirect("account:user_profile", user.id)


class EditProfileView(LoginRequiredMixin, View):
    form_class = EditProfileForm

    def get(self, request):
        form = self.form_class(instance=request.user.profile, initial={"email" : request.user.email})
        context = {
            "form" : form,
        }
        return render(request, "account/edit_profile.html", context)
    
    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data["email"]
            request.user.save()
            messages.success(request, "Your profile has been updated", "success")
            return redirect("account:user_profile", request.user.id)
