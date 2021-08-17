from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# Create your models here.

#User = get_user_model()

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email :
            raise ValueError("Vous devez entrer un email.")

        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    zip_code = models.CharField(blank=True, max_length=5)
    date_joined = models.DateField(blank=False, auto_now_add=True)
    thumbnail = models.ImageField(blank=True, verbose_name="Avatar", upload_to="avatar/")


    #age = models.IntegerField()
    #REQUIRED_FIELDS = ["age"]
    USERNAME_FIELD = "email"
    objects = MyUserManager()

    class Meta:
        verbose_name = "Utilisateur"
        ordering = ["email"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        """
            pour les groupes d'utilisateurs
        """
        return True

    def has_module_perms(self, app_label):
        """
            pour les groupes d'utilisateurs
        """
        return True

    def get_absolute_url(self):
        return reverse("posts:blog-profile", kwargs={"pk":self.pk})

class BlogCategory(models.Model):
    name = models.CharField(unique=True, max_length=255, blank=False)
    slug = models.SlugField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True, blank=False)

    class Meta:
        verbose_name = 'Categorie'
    
    def save(self, *args, **kwargs):
        if not self.slug :
           self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name="Titre")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    last_update = models.DateTimeField(auto_now_add=True)
    created_on = models.DateField(blank=True, null=True)
    published = models.BooleanField(default=False, verbose_name="Publié")
    content = models.TextField(blank=True, verbose_name="Contenu")
    thumbnail = models.ImageField(blank=True, verbose_name="Image", upload_to="blog/")
    category = models.ManyToManyField(BlogCategory)

    class Meta:
        ordering = ['-last_update']
        verbose_name = "Article"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug :
           self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def word_count(self):
        return len(self.content.split())

    def get_absolute_url(self):
        return reverse("posts:blog-post", kwargs={"pk":self.pk})

    @property
    def categorie(self):
        return ",".join([str(categorie) for categorie in self.category.all()])

    @property
    def nb_categories(self):
        return len(self.category.all())

    @property
    def author_or_default(self):
        return self.author if self.author else "auteur inconnu"

    @property
    def is_published(self):
        return "Publié" if self.published else "Non Publié"

    @property
    def is_dated(self):
        return {self.created_on} if self.created_on else "Non daté"

class BlogComment(models.Model):
    title = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(blank=True)
    content = models.TextField(blank=False)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(BlogPost, on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Commentaire"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug :
           self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("posts:blog-post", kwargs={"pk":self.post.pk})
