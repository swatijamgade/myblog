from .serializers import PostSerializer
from ..models import Post
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView


class PostListApiView(generics.ListAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer

class PostCreateApiView(generics.CreateAPIView):
    queryset = Post.published.all()
    serializer_class = PostSerializer

class PostListViews(APIView):
    def get(self, request):
        posts = Post.published.all()
        serializer = PostSerializer(instance=posts, many=True)
        data = serializer.data
        return Response(data)

class PostCreateView(APIView):
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            rsp = {"message": "Post created successfully", "status": "success", "data": serializer.data}
            return Response(rsp)
        return Response(serializer.errors)


class SharePostViaEmailAPI(APIView):
    def post(self, request):
        pass


