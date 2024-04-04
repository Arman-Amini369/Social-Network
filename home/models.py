from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=100)
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("home:post_detail", args=(self.id, self.slug))
    
    def likes_count(self):
        return self.pvotes.count()

    def can_like(self, user):
        user_like = user.uvotes.filter(post=self)
        if user_like.exists():
            return True
        else:
            return False


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ucomments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="pcomments")
    reply = models.ForeignKey("self", on_delete=models.CASCADE, related_name="rcomments", null=True, blank=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} in {self.post} have commented {self.body[:30]}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uvotes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="pvotes")

    def __str__(self):
        return f"{self.user} have liked {self.post.slug}"
