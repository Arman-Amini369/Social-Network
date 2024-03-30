from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth import views as auth_views
from .models import Post
from .forms import PostCreateUpdateForm



class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        context = {
        "posts": posts,
        }
        return render(request, "home/index.html", context)
    

class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        context = {
        "post": post,
        }
        return render(request, "home/post_detail.html", context)
    

class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, "Your Post Has Been Deleted Successfully", "success")
            return redirect("home:home")

        else:
            messages.error(request, "You Are Not Authorized To Delete This Post", "danger")
            return redirect("home:home")


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm
    template_name = "home/post_update.html"

    def setup(self, request, *args, **kwargs):
        self.post_instance = post = get_object_or_404(Post, pk=kwargs["post_id"], slug=kwargs["post_slug"])
        print('args=', args, 'kwargs=', kwargs)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.pk == request.user.pk:
            messages.error(request, "You Are Not Authorized To Update This Post", "danger")
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        context = {
            "form" : form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data["title"])
            new_post.save()
            messages.success(request, "Post Has Been Updated Successfully", "success")
            return redirect("home:post_detail", post.pk, post.slug)
        context = {
            "form" : "form",
        }
        return render(request, self.template_name, context)
    

class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        context = {
            "form" : form,
        }
        return render(request, "home/post_create.html", context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.slug = slugify(form.cleaned_data["title"])
            new_post.save()
            messages.success(request, "Your New Post Has Been Created Successfully", "success")
            return redirect("home:post_detail", new_post.pk, new_post.slug)
        