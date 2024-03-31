from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.HomeView.as_view(), name='home'),
    path("post/<int:post_id>/<slug:post_slug>/", views.PostDetailView.as_view(), name='post_detail'),
    path("post/delete/<int:post_id>/<slug:post_slug>/", views.PostDeleteView.as_view(), name="post_delete"),
    path("post/update/<int:post_id>/<slug:post_slug>/", views.PostUpdateView.as_view(), name="post_update"),
    path("post/create/", views.PostCreateView.as_view(), name="post_create"),
    path("reply/<int:post_id>/<int:comment_id>/", views.ReplyAddView.as_view(), name="reply_add"),
    path("comment/delete/<int:comment_id>", views.CommentDeleteView.as_view(), name="comment_delete"),
    path("comment/update/<int:comment_id>", views.CommentUpdateView.as_view(), name="comment_update"),
]