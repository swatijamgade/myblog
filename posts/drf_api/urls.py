from django.urls import path
from .views import PostListApiView, PostListViews, PostCreateView

app_name = 'drf_api'

urlpatterns = [
    path('posts/', PostListApiView.as_view(), name='posts_api'),
    path('posts_list/', PostListViews.as_view(), name='posts_list_api'),
    path('posts_create/', PostCreateView.as_view(), name='posts_create_'),
]
