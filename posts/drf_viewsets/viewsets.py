from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .serializers import PostSerializer

from ..models import Post


class PostViewSet(ViewSet):
    def list(self, request):
        queryset = Post.published.all()
        serializer = PostSerializer(instance=queryset, many=True)
        data = serializer.data
        return Response(data)

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            rsp = {"message": "Post created successfully", "status": "success", "data": serializer.data}
            return Response(rsp)
        return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({"message": "Post not found"})
        serializer = PostSerializer(instance=post)
        data = serializer.data
        return Response(data, status=200)

    def update(self, request, pk=None):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({"message": "Post not found"})
        serializer = PostSerializer(instance=post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            rsp = {"message": "Post updated successfully", "data": serializer.data}
            return Response(rsp)
        return Response(serializer.errors)

    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(id=pk)
        except Post.DoesNotExist:
            return Response({"message": "Post not found"})
        post.delete()
        return Response({"message": "Post deleted successfully"})