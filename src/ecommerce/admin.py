from django.contrib import admin

from ecommerce.models import Article, Category, Panier, Command, Status
# Register your models here.


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_on", "stock","price","thumbnail", "categorie")
    list_display_links = ("name",)

    empty_value_display = "-"

    search_fields = ("name", "slug",)
    list_filter = ("category",)
    filter_horizontal = ("category",)

    list_editable = ("price","stock")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug",)
    

@admin.register(Panier)
class PanierAdmin(admin.ModelAdmin):
    list_display = ("pk","title","command","article","price", "nb", "total",)
    search_fields = ("command", "article")
    list_filter = ("article", "total")


@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ("title", "total", "buyer", "get_status")
    list_filter = ("buyer",)
    filter_horizontal = ("status",)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("name", "slug",)