from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .serializers import (
    UserSerializer, AccountSerializer, DestinationSerializer,
    AccountMemberSerializer, LogSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    @swagger_auto_schema(
        operation_summary="Register new user",
        operation_description="Create a new user account with admin privileges",
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
            400: "Bad Request"
        }
    )
    def create(self, request):
        # Your existing code
        pass

class AccountViewSet(viewsets.ModelViewSet):
    @swagger_auto_schema(
        operation_summary="Create new account",
        request_body=AccountSerializer,
        responses={
            201: AccountSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden"
        },
        security=[{'Bearer': []}]
    )
    def create(self, request):
        # Your existing code
        pass

    @swagger_auto_schema(
        operation_summary="List accounts",
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by account name",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER,
                required=False
            )
        ],
        responses={200: AccountSerializer(many=True)}
    )
    def list(self, request):
        # Your existing code
        pass

class DataHandlerView(APIView):
    @swagger_auto_schema(
        operation_summary="Receive incoming data",
        operation_description="Endpoint for receiving webhook data",
        manual_parameters=[
            openapi.Parameter(
                'CL-X-TOKEN',
                openapi.IN_HEADER,
                description="App secret token",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'CL-X-EVENT-ID',
                openapi.IN_HEADER,
                description="Unique event ID",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            additional_properties=True
        ),
        responses={
            200: openapi.Response(
                description="Success",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Data Received"
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid Data",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Invalid Data"
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthenticated",
                examples={
                    "application/json": {
                        "success": False,
                        "message": "Unauthenticated"
                    }
                }
            ),
            429: "Too Many Requests"
        }
    )
    def post(self, request):
        # Your existing code
        pass

class LogViewSet(viewsets.ReadOnlyModelViewSet):
    @swagger_auto_schema(
        operation_summary="List logs",
        manual_parameters=[
            openapi.Parameter(
                'account_id',
                openapi.IN_QUERY,
                description="Filter by account ID",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'destination_id',
                openapi.IN_QUERY,
                description="Filter by destination ID",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Filter by status",
                type=openapi.TYPE_STRING,
                enum=['success', 'failed'],
                required=False
            ),
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Filter by start date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="Filter by end date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                required=False
            )
        ],
        responses={200: LogSerializer(many=True)}
    )
    def list(self, request):
        # Your existing code
        pass 