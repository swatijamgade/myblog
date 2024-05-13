from django.shortcuts import render
from .models import Post, Comment
from .forms import CommentModelForm
from django.http import HttpResponse

# http://127.0.0.1:8000/post/2024/5/8/this-is-title/?key=value&k2=value2


def post_list(request):
    posts = Post.objects.filter(status='published')
    return HttpResponse('Hello World')
    return render(request, 'posts/post-list.html', context={'all_posts': posts, 'title': 'Blog Posts'})


def post_detail(request, year, month, day, post_slug):

    post = Post.objects.get(
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post_slug
    )
    return render(request, 'posts/post-detail.html', context={'post': post})

def post_comment(request):
    """
    This function is used to handle the comment form submission
    """

    if request.method == 'POST':
        comment_form = CommentModelForm(request.POST)
        data = request.POST

        # get post by id
        post = Post.objects.get(id=data['post_id'])

        # save it
        comment = Comment(post=post, name=data['name'], email=data['email'], content=data['comment'])
        comment.save()

        # another option of saving
        # Comment.objects.create(post_id=data['post_id'], name=data['name'], email=data['email'], content=data['content'])

        # get all comments for the post
        comments = Comment.objects.filter(post=post)
        print(comments)

        return render(request, 'posts/comment.html', context={'post': post, 'comments': comments, 'form': comment_form})