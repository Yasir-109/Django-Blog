from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
from theblog.models import Post, Category
from .serializers import PostSerializer, CategorySerializer, CommentSerializer, PostUpdateSerializer, PostAddSerializer, PostLikeSerializer


class HomeAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ArticleAPIView(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        return Response(PostSerializer(post).data)
    
class AddPostAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostAddSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Associate the post with the current user


    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UpdatePostAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        return Response(PostSerializer(post).data)
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

class DeletePostAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        return Response(PostSerializer(post).data)
    
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class CategoryAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        category = self.kwargs['cat']  # Get the category from URL parameters
        return Post.objects.filter(category=category.replace("-", ' '))
    
class AddCategoryAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
class LikeAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    

# class LikeAPIView(generics.UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated]

#     def patch(self, request, *args, **kwargs):
#         post = self.get_object()
#         user = request.user

#         if post.likes.filter(id=user.id).exists():
#             post.likes.remove(user)
#             liked = False
#         else:
#             post.likes.add(user)
#             liked = True

#         serialized_post = self.serializer_class(post)
#         response_data = {
#             'liked': liked,
#             'likes_count': post.likes.count(),
#             'post': serialized_post.data
#         }
#         return Response(response_data)


class AddCommentAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def perform_create(self, serializer):
        post_id = self.kwargs['pk']
        serializer.save(post_id=post_id)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)