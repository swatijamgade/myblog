
from django.urls import path

from .views import post_list, post_detail, post_comment

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post_slug>/', post_detail, name='post_detail'),
    path('post-comment/<int:post_id>/', post_comment, name='post_comment'),
]
