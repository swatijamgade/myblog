"""
URL configuration for myblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
]

# http://127.0.0.1:8000/posts/
# http://127.0.0.1:8000/myposts/login/
# http://127.0.0.1:8000/myposts/logout/
# http://127.0.0.1:8000/
# http://127.0.0.1:8000/login/
# http://127.0.0.1:8000/logout
# http://127.0.0.1:8000/share/like
# http://127.0.0.1:8000/abc/share/