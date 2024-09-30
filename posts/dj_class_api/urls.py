from django.urls import path
from . import views

app_name = 'posts_api'

urlpatterns = [
    path('v1/post/', views.GetPostsAPI.as_view(), name='get-post-api'),
]