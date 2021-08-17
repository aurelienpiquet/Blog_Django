from django.http import request
from django.urls.base import reverse_lazy
from posts.models import BlogPost, CustomUser, BlogComment, BlogCategory
from django.shortcuts import get_object_or_404, render, redirect, resolve_url
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from posts.forms import CustomSignupForm, AvatarForm, CommentForm, SearchForm

