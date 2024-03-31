from django import forms
from .models import Post, Comment

class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "body")
    

class CommentReplyCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter your comment or reply here..."}),
        }