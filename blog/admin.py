from django.contrib import admin
from .models import Post, Profile, Comment, Category
from ckeditor.widgets import CKEditorWidget


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "author", "body", "status")
    list_filter = ("status", "created", "updated")
    search_fields = ["author__username", "title"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("status",)
    date_hierarchy = "created"


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "image")


admin.site.register(Post, PostAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Comment)
admin.site.register(Category)