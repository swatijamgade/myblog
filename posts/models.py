from django.db import models
from django.contrib.auth.models import User

# class Auther(models.Model):
#     # id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     bio = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.name


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

# one instance = one row in the table
# one field = one column in the table
# one model = one table in the database
