# imports

from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from PIL import Image
from ckeditor.fields import RichTextField


# Databases of projects
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta: 
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Post(models.Model):

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # The published manager.

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    # POST_CASTEGORY = (
    #     ("regional", "Regional"),
    #     ("scintific", "Scientific"),
    #     ("physics", "Physics"),
    #     ("chemistry", "Chemistry"),
    #     ("mathematics", "Mathematics"),
    #     ("biology", "Biology"),
    #     ("sports", "Sports"),
    #     ("ai", "AI"),
    #     ("offtopic", "Off-topic"),
    #     ("programming", "Programming"),
    #     ("datascience", "Data Science"),
    #     ("entrance_exam", "Entrance Exam"),
    #     ("travel", "Travel"),
    #     ("celebrity_talk", "Celebrity_talk"),
    #     ("world", "World"),
    #     ("astronomy", "Astronomy"),
    #     ("engineering", "Engineering"),
    #     ("technology", "Technology"),
    # )

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse("post-detail", args=[self.pk, self.slug])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profile"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment', null=True, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True, max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))









# class-based forms


class PostCreationForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body", "status"]


class PostEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "body", "status"]


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Username or Email", required=True)
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput, required=True
    )


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]


class UserUpdateForm(ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write here', 'rows': '2', 'cols': '50'}))
    class Meta:
        model = Comment
        fields = ["content"]