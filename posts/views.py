import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.views.generic import View, ListView, TemplateView, FormView
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from .models import Post, Comment
from .forms import CommentModelForm, EmailPostForm, SearchForm
from taggit.models import Tag
from django.db.models import Count


def post_list(request, tag_slug=None):
    posts = Post.objects.filter(status='published')
    paginator = None

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    try:
        posts_per_page = 3
        paginator = Paginator(object_list=posts, per_page=posts_per_page)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, template_name='posts/list.html', context={'posts': page_obj, 'tag': tag})


class PostListView(View):
    template_name = 'posts/list.html'

    def get(self, request, tag_slug=None):
        posts = Post.objects.filter(status='published')
        paginator = None

        tag = None
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            posts = posts.filter(tags__in=[tag])

        try:
            posts_per_page = 3
            paginator = Paginator(object_list=posts, per_page=posts_per_page)
            page_number = self.request.GET.get('page', 1)
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        return render(self.request, template_name=self.template_name, context={'posts': page_obj, 'tag': tag})


class HomePage(TemplateView):
    template_name = 'posts/home.html'


class PostListViewTemp(ListView):
    """
    Post.objects.all() is the default queryset
    """
    model = Post
    queryset = Post.published.all()
    template_name = 'posts/posts_list.html'  # default template name


class CommentFormView(FormView):
    form_class = CommentModelForm
    template_name = 'posts/comment.html'


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
        return render(request, '404.html')

    comments = Comment.objects.filter(post=post, active=True)
    form = CommentModelForm()
    # total_comments = comments.count()
    post_limit = 4
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:post_limit]

    context = {"post": post, "comments": comments, "form": form, "similar_posts": similar_posts}
    return render(request, template_name="posts/detail.html", context=context)


@require_POST
def post_comment(request, post_id):
    """
    This function is used to handle the comment form submission
    """
    post = get_object_or_404(Post, id=post_id)
    comment_form = CommentModelForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post  # attach post to comment
        comment.save()
        context = {'post': post, 'comment': comment, 'form': comment_form}
        return render(request, 'posts/comment.html', context=context)
    else:
        print(comment_form.errors)


def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        sent = False
        if form.is_valid():
            # get the cleaned data
            cd = form.cleaned_data
            # prepare mail sending
            # collect all mail contents
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


class SharePostView(View):
    template_name = 'posts/share.html'

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = EmailPostForm
        return render(request, self.template_name, context={'post': post, 'form': form})

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = EmailPostForm(request.POST)
        sent = False
        if form.is_valid():
            # get the cleaned data
            cd = form.cleaned_data
            # prepare mail sending
            # collect all mail contents
            post_url = self.request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject=subject, message=message, from_email=cd['email'], recipient_list=[cd['to']])
            sent = True
            return render(request, self.template_name, context={'post': post, 'form': form, 'sent': sent})
        else:
            print(form.errors)
            return HttpResponse('Form is invalid')


def search_post(request):
    """
    This function is used to search for posts
    """
    search_form = SearchForm()  # empty form

    if 'query' in request.GET:
        search_form = SearchForm(request.GET)  # submitted form
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            results = Post.published.filter(
                Q(title__icontains=query) | Q(content__icontains=query) | Q(author__username__icontains=query)
            ).distinct()
            return render(request, 'posts/search.html', context={'results': results, 'query': query})
    else:
        return render(request, 'posts/search.html', context={'form': search_form})