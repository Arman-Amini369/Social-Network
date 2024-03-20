from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Post


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        context = {
        "posts": posts,
        }
        return render(request, "home/index.html", context)
    

class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        context = {
        "post": post,
        }
        return render(request, "home/post_detail.html", context)
    

class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, "Your Post Has Been Deleted Successfully", "success")
            return redirect("home:home")

        else:
            messages.error(request, "You Are Not Authorized To Delete This Post", "danger")
            return redirect("home:home")