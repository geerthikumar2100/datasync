from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from core.models import User, Account, Role, AccountMember
from core.serializers import UserSerializer
import uuid

@api_view(["POST"])
@permission_classes([AllowAny])
def user_signup(request):
    """
    - If no user exists, create the first Admin and an associated account.
    - If users exist, only an Admin can add new users to an account.
    - If a user with the same email already exists, return an error.
    """
    # Check if user with the same email exists
    email = request.data.get("email")
    if User.objects.filter(email=email).exists():
        return Response({"error": "User with this email already exists"}, status=400)

    # existing_users = User.objects.count()
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User created successfully"}, status=201)

    return Response(serializer.errors, status=400)

@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    user = authenticate(email=email, password=password)

    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
    
    return Response({"error": "Invalid credentials"}, status=400)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    request.user.auth_token.delete()
    return Response({"message": "Logged out successfully"})
