from django.shortcuts import render
from .models import Post


def home(request):
    post = Post.objects.all()
    return render(request, 'posts/home.html', context={'all_posts': post})
