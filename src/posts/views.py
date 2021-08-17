from django.http import request
from django.urls.base import reverse_lazy
from posts.models import BlogPost, CustomUser, BlogComment, BlogCategory
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect, resolve_url
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from posts.forms import CustomSignupForm, AvatarForm, CommentForm, SearchForm

class BlogHome(ListView):
    model = BlogPost
    context_object_name = "posts"
    template_name = 'posts/index.html'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset
        else:
            return queryset.filter(published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = BlogCategory.objects.all()
        context['categories'] = categories
        context['search_form'] = SearchForm()
        return context

class Blog(DetailView):
    model = BlogPost
    context_object_name = "post"
    template_name = 'posts/blog.html'
    form_class = CommentForm
    fields = ['title','content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = BlogComment.objects.filter(post__pk=self.request.resolver_match.kwargs.get('pk'))
        context['comments'] = comments
        context['button_form'] = "Ajouter un commentaire"
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            print('on rentre dans post')
            #user_to_update = get_object_or_404(CustomUser, id=request.user.pk)
            form = CommentForm(request.POST)
            if form.is_valid():
                form.instance.author = request.user
                form.instance.post = BlogPost.objects.get(pk=self.request.resolver_match.kwargs.get('pk'))
                print('on post')
                form.save()
            return redirect('posts:blog-post', pk=self.request.resolver_match.kwargs.get('pk'))

def search_blog(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        #titles = BlogPost.objects.filter(title__contains=search)
        titles = get_list_or_404(BlogPost, title__contains=search)
        return render(request, 'posts/searches.html', context = {'titles' : titles})

def search_blog_category(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        search = request.GET.get('search')
        titles = BlogPost.objects.filter(category__name__contains=search)        
        return render(request, 'posts/searches.html', context = {'titles' : titles})

    if request.method == 'POST':
        form = SearchForm(request.POST)
        list_categories = form.data.getlist('category') 
        titles_search = get_list_or_404(BlogPost, category__in=list_categories)
        #titles_search = list(BlogPost.objects.filter(category__in=form.data.getlist('category')))
        titles = list(set([title for title in titles_search if title.nb_categories == len(list_categories)]))
        message = f"{len(titles)} article(s) ont été trouvé(s)."
        if not titles :
            titles = []
            message = "Aucun Article ne correspond à votre recherche."
        return render(request, 'posts/searches.html', context = {'titles' : titles, 'message':message})

class DeleteComment(DeleteView):
    model = BlogComment
    template_name = "posts/blogpost_crud.html"
    context_object_name = "blog"
    success_url = reverse_lazy("posts:home")
    title = "default"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['button_form'] = "Supprimer"
        context['message'] = "Voulez-vous supprimer le commentaire suivant?"
        return context


class CreateBlog(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_url = '/create/'
    model = BlogPost
    template_name = "posts/blogpost_crud.html"
    fields = ['title', 'content']
    title = "Ajouter un Post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "Voulez-vous créer un nouveau blog?"
        context['button_form'] = "Ajouter"
        return context

@method_decorator(login_required, name="dispatch")
class UpdateBlog(UpdateView):
    model = BlogPost
    template_name = "posts/blogpost_crud.html"
    context_object_name = "blog"
    fields = ['title', 'author', 'published', 'content', 'thumbnail']
    title = "Mettre à jour un blog"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = "Voulez-vous modifier le blog suivant?"
        context['button_form'] = "Mise à jour"
        return context

@method_decorator(login_required, name="dispatch")
class DeleteBlog(DeleteView):
    model = BlogPost
    template_name = "posts/blogpost_crud.html"
    context_object_name = "blog"
    success_url = reverse_lazy("posts:home")
    title = "default"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['button_form'] = "Supprimer"
        context['message'] = "Voulez-vous supprimer le blog suivant?"
        return context

def signup(request):
    context = {}
    context["button_form"] = "Créer un compte"
    context["message"] = "Formulaire de création de nouveau compte"
    context["title"] = "Création d'un nouveau compte"
    
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:home')
        else :
            context['errors'] = form.errors
    
    form = CustomSignupForm()
    context["form"] = form
    return render(request, 'accounts/connections.html', context=context)


class BlogPostLogin(LoginView):
    template_name = "accounts/connections.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context['button_form'] = "Se connecter"
        context['title'] = "Page de connection"
        context['message'] = "Page de connection"
        return context

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url('/')

class BlogPostLogout(LogoutView):
    next_page = '/'


class BlogPostUserProfil(DetailView):
    model = CustomUser
    template_name = "accounts/profil.html"
    context_object_name = "user"

class BlogPostProfilUpdate(UpdateView):
    model = CustomUser
    template_name="accounts/user_crud.html"
    form_class = AvatarForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button_form'] = "Modifier"
        return context

    def post(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            user_to_update = get_object_or_404(CustomUser, id=request.user.pk)
            form = AvatarForm(request.POST, request.FILES, instance=user_to_update)
            if form.is_valid():
                form.save()
                return redirect('posts:blog-profile', pk=request.user.pk)
        else:
            form = AvatarForm()
            context['form'] = form
            return render(request, 'accounts/user_crud.html', context=context)
 
class BlogPasswordResetView(PasswordResetView):
    model = CustomUser
    template_name = "accounts/user_crud.html"
    next_page = "/"