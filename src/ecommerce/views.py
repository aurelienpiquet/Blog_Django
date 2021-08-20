from django.http import request
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse_lazy
from ecommerce.models import Article, Status, Command, Panier, Category
from posts.models import CustomUser
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect, resolve_url
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from ecommerce.forms import CreatePanierForm, DeletePanierForm, SearchForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.

def get_panier(user):
    context = {}
    total = 0 
    commands = Command.objects.filter(buyer=user, status=6)
    paniers = [Panier.objects.filter(command=command) for command in commands] 
    context['paniers'] = paniers
    context['commands'] = commands
    for list_paniers in paniers:
        for panier in list_paniers:
            total += panier.total
    
    context['total'] = total
    context['form'] = CreatePanierForm
    context['delete_form'] = DeletePanierForm

    return context


class EcommerceHome(ListView):
    model = Article
    template_name = "ecommerce/articles.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        total = 0
        context = super().get_context_data(**kwargs)
        context['title'] = "Liste des articles à la vente."

        user = self.request.user
        context.update(get_panier(user))

        context['categories'] = get_list_or_404(Category)
        return context    

class ArticleView(DetailView):
    model = Article
    template_name = "ecommerce/article.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        total = 0
        context = super().get_context_data(**kwargs)
        context['title'] = "Page de l'article: "
        user = self.request.user
        context.update(get_panier(user))
        return context

class ListArticleView(ListView):
    model = Article
    context_object_name = "articles"

    def get(self, request, *args, **kwargs):
        context = {}
        super().get(request, *args, **kwargs)
        search = request.GET.get('search')
        articles = Article.objects.filter(category__name__contains=search)  
        context['articles'] = articles
        user = self.request.user
        context.update(get_panier(user)) 
        return render(request, 'ecommerce/searchs.html', context = context)

def CreatePanier(request, pk):
    if request.method == 'POST':
        form = CreatePanierForm(request.POST)
        if form.is_valid():
            article = get_object_or_404(Article, pk=pk)
            if article.stock >= form.instance.nb and form.instance.nb > 0 :
                new_panier = Panier.objects.create(nb=0, title="default", price=0, total=0)
                new_panier.nb = form.instance.nb
                new_panier.title = f"Pannier-{new_panier.pk}"
                new_panier.price = article.price
                new_panier.total = article.price * form.instance.nb
                new_panier.article = article
                new_panier.command = Command.objects.get(buyer=request.user, status=6) if Command.objects.get(
                    buyer=request.user, status=6) != None else Command.objects.create(buyer=request.user, status=6, title=f"Command-{Command.objects.last().pk + 1}")
                new_panier.save()
                article.stock -= form.instance.nb
                article.save()
            else:
                message = f"L'article {article} n'a plus de stock."
    else:
        form = CreatePanierForm()
    return redirect(request.META['HTTP_REFERER'])

def DeletePanier(request, pk, panier):
    if request.method == 'POST' and request.POST['nb'].isdigit():
        nb = int(request.POST['nb'])
        if nb > 0 :
            selected_panier = get_object_or_404(Panier, title=panier)
            article = get_object_or_404(Article, pk=pk)
            article.stock += nb if nb <= selected_panier.nb else selected_panier.nb
            article.save()
            selected_panier.nb -= nb
            if nb > selected_panier.nb or selected_panier.nb == 0:
                selected_panier.delete()
            else:
                selected_panier.save()
    #if request.method == 'POST':
    #    form = DeletePanierForm(request.POST)
    #    print(request.POST['delete'])
    #    selected_panier = get_object_or_404(Panier, title=panier)
    #    if form.is_valid() and form.instance.nb > 0:
    #        article = get_object_or_404(Article, pk=pk)
    #        article.stock += form.instance.nb if form.instance.nb <= selected_panier.nb else selected_panier.nb
    #        article.save()
    #        selected_panier.nb -= form.instance.nb
    #        
    #        if form.instance.nb > selected_panier.nb or selected_panier.nb == 0:
    #            selected_panier.delete()
    #        else :
    #            selected_panier.save()
    return redirect(request.META['HTTP_REFERER'])

class DeletePanierView(DeleteView):
    model = Panier
    success_url = reverse_lazy("ecommerce:home")

    def delete(self, request, *args, **kwargs):
        delete = super().delete(request, *args, **kwargs)
        article = get_object_or_404(Article, pk=request.POST.get['pk'])
        article.stock += 1
        article.save()
        print('test')
        print(article)
        return delete

