from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from core.models import User, Account, Role, AccountMember
from core.serializers import UserSerializer, LoginSerializer
import uuid
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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

@swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,
    operation_description="Login with username and password",
    responses={
        200: 'Login successful',
        400: 'Invalid credentials'
    }
)
@api_view(['POST'])
def user_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
    
    return Response({'error': 'Invalid credentials'}, status=400)

@swagger_auto_schema(
    method='post',
    operation_description="Logout (requires token authentication)",
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description='Token {your_token_here}',
            type=openapi.TYPE_STRING,
            required=True
        )
    ],
    responses={
        200: 'Logged out successfully',
        401: 'Authentication credentials were not provided'
    }
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_logout(request):
    request.user.auth_token.delete()
    return Response({"message": "Logged out successfully"})
