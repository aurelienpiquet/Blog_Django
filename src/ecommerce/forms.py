
from django import forms
from django.forms import MultiWidget
from django.forms.widgets import CheckboxSelectMultiple, NumberInput, SelectDateWidget, DateInput, DateTimeInput
from posts.models import CustomUser
from ecommerce.models import Panier, Article

import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

class CreatePanierForm(forms.ModelForm):
    #nb = forms.IntegerField(widget=NumberInput)
    class Meta:
        model = Panier
        fields = ('nb',)
        widgets = {'nb' : NumberInput(attrs={'min': '0', "placeholder" : "1"})}


class DeletePanierForm(forms.ModelForm):
    class Meta:
        model = Panier
        fields = ('nb',)
        widgets = {'nb' : NumberInput(attrs={'min': '0', "placeholder" : "1"})}

class SearchForm(forms.ModelForm):
    class Meta:
        model = Article
        required = True
        fields = ('category',)
        #categories = BlogCategory.objects.all().values()
        #cat_list = [(categorie['name'], categorie['name']) for categorie in categories]
        #print(cat_list)
        #search = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=cat_list)
        widgets = {'category' : CheckboxSelectMultiple}  