
from posts.views import BlogHome, Blog, CreateBlog, UpdateBlog, DeleteBlog, BlogPostLogin, BlogPostLogout, BlogPostUserProfil, BlogPostProfilUpdate, BlogPasswordResetView, DeleteComment
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from posts.views import signup, search_blog, search_blog_category#, upload_file

app_name = "posts"

urlpatterns = [
    path('', BlogHome.as_view(), name="home"),
    path('blog/<int:pk>/', Blog.as_view(), name="blog-post"),
    path('blog/search/', search_blog, name="blog-search"),
    path('blog/search-category', search_blog_category, name="blog-search-category"),
    path('blog/create/', login_required(CreateBlog.as_view(title="Ajouter un blog")), name="blog-post-create"),
    path('blog/update/<int:pk>/', login_required(UpdateBlog.as_view(title="Modifier un blog")), name="blog-post-update"),
    path('blog/delete/<int:pk>/', login_required(DeleteBlog.as_view(title="Supprimer un blog")), name="blog-post-delete"),
    path('blog/delete-comment/<int:pk>', login_required(DeleteComment.as_view()), name="blog-comment-delete"),
    path('compte/login/', BlogPostLogin.as_view(), name="blog-login"),
    path('compte/logout/', BlogPostLogout.as_view(), name="blog-logout"),
    path('compte/nouveau/', signup, name="blog-signup"),
    path('compte/profil/<int:pk>/', login_required(BlogPostUserProfil.as_view()), name="blog-profile"),
    path('compte/profil/<int:pk>/change-avatar/', login_required(BlogPostProfilUpdate.as_view()), name="blog-avatar"),
    path('compte/profil/<int:pk>/change-password/', login_required(BlogPasswordResetView.as_view()), name="blog-password"),

    #path('compte/profil/<int:pk>/change-avatar/', login_required(upload_file), name="blog-avatar"),
    #path('compte/profil/change-avatar/', upload_file, name="blog-avatar"),
    #path('compte/connexion', signup, name="signup"),
    #path('compte/deconnexion', signup, name="signup"),
]