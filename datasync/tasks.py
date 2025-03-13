import requests
from celery import shared_task
from django.utils.timezone import now
from core.models import Destination, Log

@shared_task
def send_data_to_destination(destination_id, event_id, data):
    """
    Celery Task: Sends data to a destination asynchronously and logs the result.
    """
    try:
        destination = Destination.objects.get(id=destination_id)
        headers = destination.headers.copy()  # Get stored headers
        headers["CL-X-EVENT-ID"] = event_id  # Include event ID in request

        if destination.http_method == "GET":
            response = requests.get(destination.url, headers=headers, params=data)
        else:  # POST, PUT
            response = requests.request(destination.http_method, destination.url, headers=headers, json=data)

        status = "success" if response.status_code in [200, 201] else "failed"

    except Exception as e:
        status = "failed"
    print(f'{status=} {event_id=} ')
    # ✅ Log the Attempt
    Log.objects.create(
        event_id=event_id,
        account=destination.account,
        destination=destination,
        received_timestamp=now(),
        processed_timestamp=now(),
        received_data=data,
        status=status
    )
