from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, BlogPost, Post, Comment, UserProfile, Tag

# ✅ Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'author', 'category', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

# ✅ Post Serializer
# serializers.py
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'category', 'author']
        extra_kwargs = {
            'category': {'required': False},
            'author': {'required': False}
        }   

# ✅ Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()  # Return username instead of ID
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())  # Ensure valid post selection

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at']

# ✅ UserProfile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Display the username instead of ID

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio']

# ✅ Tag Serializer
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

# ✅ User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


