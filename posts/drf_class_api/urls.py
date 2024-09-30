from django.urls import path
from .views import (
    PostCreateView, PostListViews, PostAPIVIew, SharePostViaEmailAPI, GetPostWithTagsAPI, GetTotalPostsAPI,
    GetPostCommentsAPI, SearchPostAPI, AddCommentAPI
)


app_name = 'drf_class_api'

urlpatterns = [
    path('posts/', PostListViews.as_view(), name='posts_api'),
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('post/<int:post_id>/', PostAPIVIew.as_view(), name='post_api'),
    path('share-post/', SharePostViaEmailAPI.as_view(), name='share_post'),
    #####################################################################
    path('post-with-tags/', GetPostWithTagsAPI.as_view(), name='post_with_tags'),
    path('total-posts/', GetTotalPostsAPI.as_view(), name='total_posts'),
    path('post-comments/', GetPostCommentsAPI.as_view(), name='post_comments'),
    path('search-post/', SearchPostAPI.as_view(), name='search_post'),
    path('add-comment/<int:post_id>', AddCommentAPI.as_view(), name='add_comment'),


]


