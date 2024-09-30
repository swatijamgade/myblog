from django import template
from django.db.models import Count

from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag("posts/latest_posts.html")
def show_latest_post(count=4):
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    posts = Post.published.annotate(total_comments=Count('comments')).order_by("-total_comments")[:count]
    return posts  # queryset


@register.filter
def my_filter(input_text):
    return f"123 {input_text}"