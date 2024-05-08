from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique_for_date='publish')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    publish = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_post_title(self):
        return self.title

    def get_post_content(self):
        return self.content

    class Meta:
        ordering = ('-created',)


p1 = Post()
# one instance = one row in the table
# one field = one column in the table
# one model = one table in the database


# Spring MVC
# M - model
# V - view
# C - controller

# Django
# M - model
# V - view
# T - template


# class Comments(models.Model):
#     post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     content = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#     active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.name
