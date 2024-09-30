from django.views.generic import View
from django.http import JsonResponse

from .. models import Post


class GetPostsAPI(View):

    def get(self, request):
        posts = Post.published.all()
        post_count = posts.count()

        post_list = []

        for post in posts:
            data = {
                "title": post.title,
                "slug": post.slug,
                "body": post.body,
                "author": post.author.username
            }
            post_list.append(data)

        response = {
            "message": "Success",
            "status_code": 1,
            "data": post_list
        }

        return JsonResponse(data=response, status=200)