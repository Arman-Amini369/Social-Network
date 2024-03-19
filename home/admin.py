from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    list_filter = ("user", 'created', 'updated')
    search_fields = ('title', 'body', 'user')
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("user",)