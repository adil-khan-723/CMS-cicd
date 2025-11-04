from django.urls import path
from .views import (
    test_view, CategoryListCreateView, CategoryRetrieveUpdateDestroyView, 
    BlogPostListCreateView, BlogPostRetrieveUpdateDestroyView, PostListCreateView, 
    PostRetrieveUpdateDestroyView, CommentListCreateView, CommentRetrieveUpdateDestroyView, 
    TagListView, TagRetrieveUpdateDestroyView, UserListView, UserRetrieveView, 
    get_logged_in_user, create_blog, PublishBlogView, get_posts, create_normal_blog
)
from django.http import JsonResponse
def api_root(request):
    return JsonResponse({"message": "Welcome to the CMS API!"})

urlpatterns = [ 
    path('', api_root, name='api-root'),  # 👈 Add this
    path('test/', test_view, name='test-view'),

    # ✅ Category URLs
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-retrieve-update-destroy'),

    # ✅ BlogPost URLs
    path('blogposts/', BlogPostListCreateView.as_view(), name='blogpost-list-create'),
    path('blogposts/<int:pk>/', BlogPostRetrieveUpdateDestroyView.as_view(), name='blogpost-retrieve-update-destroy'),

    # ✅ Post URLs
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-retrieve-update-destroy'),

    # ✅ Comment URLs
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-retrieve-update-destroy'),

    # ✅ Tag URLs
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/<int:pk>/', TagRetrieveUpdateDestroyView.as_view(), name='tag-retrieve-update-destroy'),

    # ✅ User URLs
    path('users/', UserListView.as_view(), name='user-list'),  # 🔥 GET all users
    path('users/<int:pk>/', UserRetrieveView.as_view(), name='user-detail'),  # 🔥 GET specific user by ID
    path('users/me/', get_logged_in_user, name='get-logged-in-user'),  # 🔥 Fetch logged-in user

    # ✅ Blog Creation
    path('create-blog/', create_blog, name='create_blog'),
    path('normal/', create_normal_blog, name='create-normal-blog'),

    path("publish/", PublishBlogView.as_view(), name="publish_blog"),
    path('posts/', get_posts, name='get_posts'),


]
    