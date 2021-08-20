from ecommerce.views import EcommerceHome
from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from ecommerce.views import CreatePanier, DeletePanier, DeletePanierView, ArticleView, ListArticleView#, search_article_category

app_name = "ecommerce"

urlpatterns = [
    path('', EcommerceHome.as_view(), name="home"),
    path('article/<str:slug>/', ArticleView.as_view(), name="ecommerce-article"),
    path('article/search', ListArticleView.as_view(), name="search-category"),
    path('create_panier/<int:pk>', CreatePanier, name="create-panier"),
    path('delete_panier/<panier>/<int:pk>/', DeletePanier, name="delete-panier"),

]