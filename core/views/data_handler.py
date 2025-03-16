from django_ratelimit.decorators import ratelimit
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from core.models import Account, Destination, Log
from datasync.tasks import send_data_to_destination

@ratelimit(key="ip", rate="5/s", method="POST", block=True)  # ⏳ Limit 5 requests per second
@api_view(["POST"])
@permission_classes([AllowAny])
def incoming_data(request):
    """
    API to receive JSON data, validate headers, enforce rate limiting,
    and trigger async tasks to send data to destinations.
    """

    secret_token = request.headers.get("CL-X-TOKEN")
    event_id = request.headers.get("CL-X-EVENT-ID")

    if not secret_token or not event_id:
        return Response({"success": False, "message": "Unauthenticated"}, status=401)

    account = get_object_or_404(Account, app_secret_token=secret_token)

    if not isinstance(request.data, dict):
        return Response({"success": False, "message": "Invalid Data"}, status=400)
    
    data = request.data
    destinations = account.destinations.all()  # Fetch all destinations for the account

    # ✅ Send Data to All Destinations Using Async Celery Task
    for destination in destinations:
        send_data_to_destination.delay(destination.id, event_id, data)

    return Response({"success": True, "message": "Data Received"}, status=200)
