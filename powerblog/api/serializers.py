from rest_framework import serializers
from theblog.models import Post, Category, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'title_tag', 'header_image', 'snippet', 'category','body']

class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'title_tag', 'header_image', 'body']

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['likes']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['name', 'body']