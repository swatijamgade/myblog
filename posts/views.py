from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def home(request):
    post = [
        {
            'author': 'John Doe',
            'title': 'Blog Post 1',
            'content': 'First post content',
            'date_posted': 'August 27, 2021'
        },
        {
            'author': 'Jane Doe',
            'title': 'Blog Post 2',
            'content': 'Second post content',
            'date_posted': 'August 28, 2021'
        },
        {
            'author': 'Jane Doe',
            'title': 'Blog Post 2',
            'content': 'Second post content',
            'date_posted': 'August 28, 2021'
        },
        {
            'author': 'Jane Doe',
            'title': 'Blog Post 2',
            'content': 'Second post content',
            'date_posted': 'August 28, 2021'
        }
    ]

    return render(request, 'posts/home.html', context={'all_posts': post})


