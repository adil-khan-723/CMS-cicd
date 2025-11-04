import json
from rest_framework import generics, status, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Category, BlogPost, Post, Comment, Tag
from .serializers import (
    CategorySerializer, BlogPostSerializer, PostSerializer, CommentSerializer,
    TagSerializer, UserSerializer
)
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# ✅ Test API Endpoint
def test_view(request):
    return JsonResponse({"message": "Hello from Django API!"})

# ✅ Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class BlogPostListCreateView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogPostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]

# ✅ Post Views
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

# ✅ Comment Views
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

# ✅ Tag Views
class TagListView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]

class TagRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]

# ✅ User Views
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserRetrieveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# ✅ Fetch Logged-in User Details
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_logged_in_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

# ✅ Create Blog API
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_blog(request):
    if 'title' not in request.data or 'content' not in request.data:
        return Response({"error": "Missing required fields: title, content"}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data
    author_name = request.user.username  # Get logged-in user's username

    try:
        post = Post.objects.create(
            title=data['title'],
            content=data['content'],
            author=author_name  # Store the author name as string
        )
        return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_normal_blog(request):
    # Check for required fields
    required_fields = ['title', 'content', 'category', 'author_name']
    if not all(field in request.data for field in required_fields):
        return Response(
            {"error": "Missing required fields: title, content, category, author_name"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    data = request.data
    user = request.user  # Get logged-in user (for tracking purposes if needed)

    try:
        post = BlogPost.objects.create(
            title=data['title'],
            content=data['content'],
            author=data['author_name'],  # Use the provided author name
            category=data['category'],   # Use the provided category
            # Optional: You might want to track the actual user who created it
            # created_by=user  
        )
        return Response(BlogPostSerializer(post).data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ✅ Check if Email Exists API
@api_view(['GET'])
@permission_classes([AllowAny])
def check_user_exists(request):
    email = request.GET.get('email', '').strip()  # 🔥 Strip spaces and newlines

    print("Received email:", repr(email))  # Debugging log

    if not email:
        return JsonResponse({'error': 'Email is required'}, status=400)

    exists = User.objects.filter(email__iexact=email).exists()
    
    print("Database check result:", exists)  # Debugging log
    return JsonResponse({'exists': exists})

# ✅ Signup API (Corrected)
@method_decorator(csrf_exempt, name='dispatch')
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            # ✅ Use request.data (DRF automatically parses JSON)
            data = request.data  
            
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not email or not password:
                return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

            # ✅ Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            return Response({'message': 'User registered successfully!', 'user_id': user.id}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class PublishBlogView(APIView):
    def post(self, request):
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Require authentication
def get_posts(request):
    posts = BlogPost.objects.all().order_by('-id')
    serializer = BlogPostSerializer(posts, many=True)
    return Response(serializer.data)


class PostUpdateAPIView(generics.UpdateAPIView):    
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)