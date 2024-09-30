from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from .serializers import PostSerializer, PostTitleSerializer
from ..models import Post, Comment

@api_view(['GET', 'POST'])
def post_api_view(request):

    if request.method == 'GET':
        posts = Post.published.all()
        serializer = PostSerializer(instance=posts, many=True)
        data = serializer.data
        return Response(data, status=HTTP_200_OK)

    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            rsp = {"message": "Post created successfully", "status": "success", "data": serializer.data}
            return Response(rsp, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def post_detail_api_view(request, post_id):

    # post = get_object_or_404(Post, id=post_id)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"message": "Post not found"}, status=HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = PostSerializer(instance=post)
        data = serializer.data
        return Response(data, status=HTTP_200_OK)

    if request.method == 'PUT':
        serializer = PostSerializer(instance=post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            rsp = {"message": "Post updated successfully", "data": serializer.data}
            return Response(rsp, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        post.delete()
        return Response({"message": "Post deleted successfully"}, status=HTTP_200_OK)

# CRUD