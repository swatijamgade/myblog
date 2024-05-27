from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import CommentModelForm, EmailPostForm
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail


def post_list(request):
    posts = Post.objects.filter(status='published')

    paginator = None
    try:
        posts_per_page = 2
        paginator = Paginator(object_list=posts, per_page=posts_per_page)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # page_obj.has_next()
    # page_obj.previous_page_number()
    # page_obj.next_page_number()
    # page_obj.paginator.num_pages
    # page_obj.number

    return render(request, 'posts/post-list.html',
                  context={'page_obj': page_obj, 'title': 'Blog Posts', 'posts': posts})


def post_detail(request, year, month, day, post_slug):
    try:
        post = Post.objects.get(
            publish__year=year,
            publish__month=month,
            publish__day=day,
            slug=post_slug,
            status='published'
        )
    except Post.DoesNotExist:
        return HttpResponse('<h1>Post not found</h1>')

    comments = Comment.objects.filter(post=post, active=True)
    # total_comments = comments.count()
    form = CommentModelForm()
    context = {'post': post, 'comments': comments, 'form': form}
    return render(request, 'posts/post-detail.html', context=context)


def post_comment(request, post_id):
    """
    This function is used to handle the comment form submission
    """
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        comment_form = CommentModelForm(request.POST);
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


def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        sent = False
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject=subject, message=message, from_email=cd['email'], recipient_list=[cd['to']])
            sent = True
            return render(request, 'posts/share.html', context={'post': post, 'form': form, 'sent': sent})
        else:
            print(form.errors)
            return HttpResponse('Form is invalid')
    else:
        form = EmailPostForm()
        return render(request, 'posts/share.html', context={'post': post, 'form': form})

def search_post(request):
    """
    This function is used to search for posts
    """
    query = request.GET.get('query')

    # get all related posts form db
    searched_posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query) | Q(author__username__icontains=query)
    ).distinct()
    # Post.objects.filter(title__icontains=query)
    # Post.objects.filter(content__icontains=query)
    return render(request, 'posts/search.html', context={'posts': searched_posts, 'query': query})