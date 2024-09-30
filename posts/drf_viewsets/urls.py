from django.urls import path
from rest_framework import routers
from .viewsets import PostViewSet

router = routers.SimpleRouter()
router.register(r'posts-viewset', PostViewSet, basename='posts-viewset')
app_name = 'drf_viewsets'

urlpatterns = router.urls