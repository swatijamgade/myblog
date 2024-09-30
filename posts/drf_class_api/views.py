from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from ..models import Post
from .serializers import (
    PostSerializer, PostWithTagsSerializer, PostWithCommentsSerializer, SharePostSerializer, AddPostCommentSerializer
)


class PostListViews(APIView):
    def get(self, request):
        posts = Post.published.all()
        serializer = PostSerializer(instance=posts, many=True)
        data = serializer.data
        return Response(data, status=200)


class PostCreateView(APIView):
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            rsp = {"message": "Post created successfully", "status": "success", "data": serializer.data}
            return Response(rsp, status=201)
        return Response(serializer.errors, status=400)


class PostAPIVIew(APIView):

    def get_object(self, post_id):
        try:
            return Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"message": "Post not found"}, status=400)

    def get(self, request, post_id):
        post = self.get_object(post_id)
        serializer = PostSerializer(instance=post)
        data = serializer.data
        return Response(data, status=200)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            rsp = {"message": "Post created successfully", "status": "success", "data": serializer.data}
            return Response(rsp, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, post_id):
        post = self.get_object(post_id)
        serializer = PostSerializer(instance=post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            rsp = {"message": "Post updated successfully", "data": serializer.data}
            return Response(rsp, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, post_id):
        post = self.get_object(post_id)
        post.delete()
        return Response({"message": "Post deleted successfully"}, status=200)


class SharePostViaEmailAPI(APIView):
    """
    This API is used to share post via email
    """

    def post(self, request, post_id):
        post = Post.published.get(id=post_id)

        serializer = SharePostSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        name = serializer.validated_data.get('name')
        email = serializer.validated_data.get('email')
        to = serializer.validated_data.get('to')
        comments = serializer.validated_data.get('comments')

        # send email
        post_url = self.request.build_absolute_uri(post.get_absolute_url())
        subject = f"{name} recommends you read {post.title}"
        message = f"Read {post.title} at {post_url}\n\n{name}'s comments: {comments}"
        send_mail(subject=subject, message=message, from_email=[email], recipient_list=[to])


class AddCommentAPI(APIView):
    """
    Add comment to a post identified by post_id
    """

    def post(self, request, post_id):
        post = Post.published.get(id=post_id)

        # get comment data from request body
        comment_data = request.data
        serializer = AddPostCommentSerializer(data=comment_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        name = serializer.validated_data.get('name')
        email = serializer.validated_data.get('email')
        content = serializer.validated_data.get('content')

        # add comment
        comment = post.comments.create(name=name, email=email, content=content)
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
        return Response(response_data, status=201)


class SearchPostAPI(APIView):
    """
    query
    """

    def get(self, request):
        query = request.query_params.get('query')

        if not query:
            return Response({"message": "Query parameter is required"}, status=400)

        results = Post.published.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(author__username__icontains=query)
        ).distinct()

        serializer = PostSerializer(instance=results, many=True)
        data = serializer.data
        return Response(data, status=200)


class GetPostWithTagsAPI(APIView):
    """
    tag_name
    """

    def get(self, request):
        posts = Post.published.all()
        serializer = PostWithTagsSerializer(instance=posts, many=True)
        data = serializer.data
        return Response(data, status=200)


class GetTotalPostsAPI(APIView):
    """
    This API is used to get the total number of posts
    """

    def get(self, request):
        posts = Post.published.all()
        total_posts = posts.count()
        data = {"total_posts": total_posts}
        return Response(data, status=200)


class GetPostCommentsAPI(APIView):
    """
    post_id
    post = Post.published.get(id=post_id)
    comments = post.comments.all()
    """

    def get(self, request):
        posts = Post.published.all()
        serializer = PostWithCommentsSerializer(instance=posts, many=True)
        data = serializer.data
        return Response(data, status=200)
