
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import MultiWidget
from django.forms.widgets import CheckboxSelectMultiple
from posts.models import BlogCategory
from posts.models import CustomUser,BlogComment, BlogCategory, BlogPost


class CustomSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email","thumbnail")
        #fields = UserCreationForm.Meta.fields


class AvatarForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("thumbnail",)
        #exclude = ["title"] --> tout les champs sauf title

class CommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ("title", "content",)
        required = True

class SearchForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        required = True
        fields = ('category',)
        #categories = BlogCategory.objects.all().values()
        #cat_list = [(categorie['name'], categorie['name']) for categorie in categories]
        #print(cat_list)
        #search = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=cat_list)
        widgets = {'category' : CheckboxSelectMultiple}   


