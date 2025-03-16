from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from core.permissions import IsAdminOrReadOnly
from core.models import Account, Destination, AccountMember, Log
from core.serializers import AccountSerializer, DestinationSerializer, AccountMemberSerializer, LogSerializer, UserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

class AccountViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Accounts.
    Only Admins can create, update, and delete accounts.
    Normal users can only view accounts they belong to.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Account.objects.all()
        return Account.objects.filter(members__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class DestinationViewSet(viewsets.ModelViewSet):
    """
    CRUD API for Destinations.
    Only Admins can modify.
    Normal users can read and update destinations linked to their accounts.
    """
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        return Destination.objects.filter(account__members__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class AccountMemberViewSet(viewsets.ModelViewSet):
    """
    API for managing Account Members.
    Only Admins can add/remove members.
    """
    queryset = AccountMember.objects.all()
    serializer_class = AccountMemberSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        return AccountMember.objects.filter(account__members__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_account_destinations(request, account_id):
    """
    Fetch all destinations linked to a specific account.
    Only users who belong to the account can access this.
    """
    account = get_object_or_404(Account, id=account_id, members__user=request.user)
    destinations = Destination.objects.filter(account=account).values("id", "url", "http_method")
    return Response({"destinations": list(destinations)})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_logs(request, account_id):
    """
    Fetch logs for an account with optional filtering.
    Users can only view logs for accounts they belong to.
    """
    account = get_object_or_404(Account, id=account_id, members__user=request.user)
    logs = Log.objects.filter(account=account)

    # Optional filters
    filters = {}
    if request.GET.get("destination_id"):
        filters["destination__id"] = request.GET.get("destination_id")
    if request.GET.get("status"):
        filters["status"] = request.GET.get("status")
    if request.GET.get("received_timestamp"):
        filters["received_timestamp__gte"] = request.GET.get("received_timestamp")
    if request.GET.get("processed_timestamp"):
        filters["processed_timestamp__lte"] = request.GET.get("processed_timestamp")

    logs = logs.filter(**filters).values("event_id", "received_timestamp", "processed_timestamp", "status")

    return Response({"logs": list(logs)})
