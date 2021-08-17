
from django.contrib import admin

from posts.models import BlogPost, CustomUser, BlogCategory, BlogComment
# Register your models here.


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "author", "last_update", "created_on", "published","thumbnail", "categorie")
    list_display_links = ("title",)
    list_editable = ("published",)

    empty_value_display = "-"

    search_fields = ("title", "slug",)
    list_filter = ("author", "published","category")
    filter_horizontal = ("category",)
    autocomplete_fields = ("author",)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ("email",)
    list_display = ("email", "last_login", "is_staff", "is_active", "is_admin", "thumbnail")

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_on",)
    list_editatble = ("name")

@admin.register(BlogComment)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created_on", "author", "post")
    list_editatble = ("name")

    list_filter =('post',)


