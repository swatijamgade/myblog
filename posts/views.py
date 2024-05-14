from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import CommentModelForm
from django.http import HttpResponse


# http://127.0.0.1:8000/post/2024/5/8/this-is-title/?key=value&k2=value2


def post_list(request):
    posts = Post.objects.filter(status='published')
    return render(request, 'posts/post-list.html', context={'all_posts': posts, 'title': 'Blog Posts'})


def post_detail(request, year, month, day, post_slug):
    try:
        post = Post.objects.get(
            publish__year=year,
            publish__month=month,
            publish__day=day,
            slug=post_slug
        )
    except Post.DoesNotExist:
        return HttpResponse('<h1>Post not found</h1>')

    comments = Comment.objects.filter(post=post)
    form = CommentModelForm()
    context = {'post': post, 'comments': comments, 'form': form}
    return render(request, 'posts/post-detail.html', context=context)


def post_comment(request, post_id):
    """
    This function is used to handle the comment form submission
    """

    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        comment_form = CommentModelForm(request.POST)
        print(comment_form)
        print(type(comment_form))  # Post
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            print(type(comment_form))
            comment.post = post  # attach post to comment
            comment.save()
        else:
            print(comment_form.errors)

        context = {'post': post, 'comment': comment, 'form': comment_form}

        return render(request, 'posts/comment.html', context=context)
    else:
        comment_form = CommentModelForm()
        context = {'post': post, 'form': comment_form}
        return render(request, 'posts/comment.html', context=context)