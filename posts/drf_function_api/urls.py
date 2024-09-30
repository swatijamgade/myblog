from django.urls import path
from .views import post_api_view, post_detail_api_view

app_name = 'drf_function_api'

urlpatterns = [
    path('posts/', post_api_view, name='posts_api'),
    path('post/<int:post_id>/', post_detail_api_view, name='post_api'),
]