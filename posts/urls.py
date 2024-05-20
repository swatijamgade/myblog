from django.urls import path

from .views import post_list, post_detail, post_comment, share_post

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post_slug>/', post_detail, name='post_detail'),
    path('<int:post_id>/comment/', post_comment, name='post_comment'),
    path('<int:post_id>/share/', share_post, name='share_post'),

]