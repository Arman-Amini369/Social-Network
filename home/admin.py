from django.contrib import admin
from .models import Post, Comment, Vote

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    list_filter = ("user", 'created', 'updated')
    search_fields = ('title', 'body', 'user')
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("user",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "is_reply", "created")
    list_filter = ("user", "created", "post", "created")
    search_fields = ("user", "body", "post", "is_reply")
    raw_id_fields = ("user", "post", "reply")


admin.site.register(Vote)