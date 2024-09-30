import json

from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from posts.models import Post, Comment


def post_list_api(request):
    """
    This function is used to return all posts in JSON format
    """
    posts = Post.published.all()
    # serialize
    data = {"posts": list(posts.values())}
    return JsonResponse(data=data, status=200)


def posts_with_comments_api(request):
    """
    This function is used to return all posts with comments in JSON format
    """
    posts = Post.published.all()
    data = []
    for post in posts:
        # post is model object
        comments = post.comments.filter(active=True)  # queryset

        post_data = {
            "post": post.title,
            "comments": list(comments.values('name', 'email', 'content'))
        }

        data.append(post_data)

    return JsonResponse(data=data, status=200, safe=False)


def list_comments_api(request):
    """
    This function is used to list all comments in JSON format
    """
    comments = Comment.objects.all()
    data = serializers.serialize(format='json', queryset=comments)
    return HttpResponse(content=data, status=200, content_type='application/json')


@csrf_exempt
def add_comment_api(request):
    """
    This function is used to add a comment to a post
        {
        "post_id": 1,
        "comment": {
            "name": "xyz",
            "email": "xyz@email.com",
            "content": "This is comment from api"
        }
    }
    """
    request_body = request.body.decode('utf-8')
    request_dict = json.loads(request_body)

    # get post
    post_id = request_dict.get('post_id')
    post = Post.published.get(id=post_id)

    # create comment
    comment_data = request_dict.get('comment')
    comment = Comment(post=post, **comment_data)
    comment.save()
    response_data = {
        "message": "success",
        "post": post.title,
        "comment": {
            "id": comment.id,
            "name": comment.name,
            "email": comment.email,
            "content": comment.content
        }
    }
    return JsonResponse(response_data, safe=False, status=201)


@csrf_exempt
def create_post_api(request):
    # get payload
    string_body = request.body.decode("UTF-8")
    json_body = json.loads(string_body)

    # create Post object
    title = json_body['title']
    body = json_body['body']
    author = User.objects.get(username=json_body['author'])
    post = Post.objects.create(title=title, author=author, body=body)

    data = {
        "message": f"post has been created successfully, with id {post.id}"
    }
    return JsonResponse(data=data, status=201)


@csrf_exempt
def update_post_api(request, post_id):
    # get payload
    string_body = request.body.decode("UTF-8")
    body_dict = json.loads(string_body)
    post_title = body_dict["title"]

    try:
        # update post
        post = Post.published.get(id=post_id)
        post.title = post_title
        post.save()
    except Post.DoesNotExist:
        data = {"error": f"post does not exist, with given id {post_id}"}
        return JsonResponse(data=data, status=404)

    data = {
        "message": f"post has been updated successfully, with id {post.id}"
    }
    return JsonResponse(data=data, status=200)


@csrf_exempt
def delete_post_api(request, post_id):
    try:
        # update post
        post = Post.published.get(id=post_id)
        post.delete()
    except Post.DoesNotExist:
        data = {"error": "post does not exist"}
        return JsonResponse(data=data, status=404)

    data = {"message": f"post has been deleted successfully, with id {post_id}"}
    return JsonResponse(data=data, status=200)