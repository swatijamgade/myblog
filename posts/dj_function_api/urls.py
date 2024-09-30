from django.urls import path

from .views import (
    post_list_api, posts_with_comments_api, list_comments_api, add_comment_api, create_post_api, update_post_api, delete_post_api
)

app_name = 'posts_api'

urlpatterns = [
    # api
    path('v1/posts/', post_list_api, name='post_list_api'),
    path('v2/posts/', posts_with_comments_api, name='post_list_api_v2'),
    path('v1/comments/', list_comments_api, name='list_comments'),
    path('v1/comments/add/', add_comment_api, name='add_comment_api'),
    path('posts/', create_post_api, name='create-post'),
    path('posts/<int:post_id>/', update_post_api, name='update-post'),
    path('posts/<int:post_id>/', delete_post_api, name='delete-post'),

]