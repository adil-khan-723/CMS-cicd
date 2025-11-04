from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
# import json
import logging
from django.contrib.auth.hashers import make_password
logger = logging.getLogger(__name__)

# ✅ Check if a username exists
@api_view(['POST'])
@permission_classes([AllowAny])
def check_user_exists(request):
    username = request.data.get('username', '').strip()

    if not username:
        return Response({"error": "Username is required"}, status=400)

    user_exists = User.objects.filter(username=username).exists()
    return Response({"exists": user_exists})


@api_view(["POST"])
def user_login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user:
        token, created = Token.objects.get_or_create(user=user)  # ✅ Ensures the user keeps the same token
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# ✅ Logout API (Token-based logout)
@api_view(['POST'])
def user_logout(request):
    if request.user.is_authenticated:
        try:
            request.user.auth_token.delete()  # Delete user's token
            logout(request)
            return Response({"message": "Logged out successfully"}, status=200)
        except Exception as e:
            logger.error(f"Logout error: {e}")
            return Response({"error": "Logout failed"}, status=500)
    return Response({"error": "User is not authenticated"}, status=400)


# ✅ Signup API (Now username-based)
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()

        if not username or not password:
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        token, created = Token.objects.get_or_create(user=user)

        return Response({'message': 'User registered successfully', 'token': token.key}, status=status.HTTP_201_CREATED)

@api_view(["GET"])
def profile_view(request):
    if request.user.is_authenticated:
        return Response({"username": request.user.username, "email": request.user.email})
    return Response({"error": "Unauthorized"}, status=401)


@api_view(['POST'])
def reset_password(request):
    username = request.data.get('username')
    new_password = request.data.get('new_password')

    if not username or not new_password:
        return Response({'error': 'Username and new password are required.'}, status=400)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)

    user.password = make_password(new_password)
    user.save()

    return Response({'message': 'Password reset successfully!'}, status=200)