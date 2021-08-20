from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.http import request
from posts.models import CustomUser
from django.shortcuts import get_object_or_404
from django.core.validators import MinValueValidator, MaxValueValidator

import datetime
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name="Nom")
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name = "Categorie"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug :
           self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Status(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name = 'Statu'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug :
           self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Article(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='Article')
    slug = models.SlugField(blank=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name="Description")
    stock = models.IntegerField(blank=False, verbose_name="Stock")
    created_on = models.DateTimeField(blank=True, verbose_name="Date")
    category = models.ManyToManyField(Category, blank=True)
    thumbnail = models.ImageField(blank=True, verbose_name="Image", upload_to='ecommerce')
    price = models.FloatField(blank=True, verbose_name="Prix", default=0)


    class Meta:
        ordering = ['-created_on']
        verbose_name = "Article"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug :
           self.slug = slugify(self.name)
        self.created_on = datetime.datetime.now() if not self.created_on else self.created_on
        super().save(*args, **kwargs)

    @property
    def categorie(self):
        return ", ".join([str(categorie) for categorie in self.category.all()])

class Command(models.Model):
    title = models.CharField(max_length=255, blank=False, verbose_name="Commande")
    total = models.FloatField(blank=True, null=True, verbose_name="Total")
    buyer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ManyToManyField(Status, blank=True, verbose_name="Status", default="Aucun")

    class Meta:
        verbose_name = "Command"

    def __str__(self):
        return self.title

    @property
    def get_status(self):
        return ", ".join([str(status) for status in self.status.all()])

class Panier(models.Model):
    title = models.CharField(unique=True, max_length=255, null=True, verbose_name="Numéro de panier")
    nb = models.PositiveIntegerField(blank=False, verbose_name="Nombre")
    price = models.FloatField(blank=False, verbose_name="Prix", default=0)
    total = models.FloatField(verbose_name="Total", blank=True)
    article = models.ForeignKey(Article, blank=False, verbose_name="Article", on_delete=models.SET_NULL, null=True)
    command = models.ForeignKey(Command, blank=False, verbose_name="Commande", on_delete=models.SET_NULL, null=True)
    
    count = 0
    
    class Meta:
        ordering=['-nb']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.total = abs(self.nb) * self.price
        super().save(*args, **kwargs)

    @property
    def get_stock(self):
        print(self.article.stock)
        return self.article.stock
    
    @property
    def get_count(self):
        return len(self.title.all())


    