from django.contrib import admin
from .models import Post, Comment
from .models import Post, Comment, Entry, Blog, Author

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Entry)
admin.site.register(Blog)
admin.site.register(Author)