from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.text import slugify
from datetime import date
from taggit.managers import TaggableManager


class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class TotalPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().count()


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique_for_date='publish')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    publish = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    tags = TaggableManager()

    # custom manger
    objects = models.Manager()  # default manager
    published = PublishManager()  # custom manager
    total_posts = TotalPostManager()  # custom manager

    def __str__(self):
        return self.title

    def get_post_title(self):
        return self.title

    def get_post_content(self):
        return self.content

    class Meta:
        ordering = ('-created',)

    def get_absolute_url(self):
        # return f'/post/{self.publish.year}/{self.publish.month}/{self.publish.day}/{self.slug}/'
        return reverse('posts:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        slug = slugify(self.title)
        self.slug = slug
        super().save(force_insert, force_update, using, update_fields)

    @classmethod
    def get_total_posts(cls):
        return cls.objects.count()

    @classmethod
    def get_latest_post(cls):
        return cls.objects.latest('-publish')


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


class Comment(models.Model):
    """
    c = Comment.objects.get(id=1)
    c.post

    p = Post.object.get(id=1)
    p.comments.all()
    """
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ('-created',)
        indexes = [
            models.Index(fields=['created', 'active']),
        ]


class Album(models.Model):
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)


class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.IntegerField()

    class Meta:
        unique_together = ['album', 'order']
        ordering = ['order']

    def __str__(self):
        return '%d: %s' % (self.order, self.title)

   gogog