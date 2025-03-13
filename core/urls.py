from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views.auth_views import user_signup, user_login, user_logout
from core.views.api_views import AccountViewSet, DestinationViewSet, AccountMemberViewSet, get_account_destinations, get_logs
from core.views.data_handler import incoming_data

router = DefaultRouter()
router.register(r"accounts", AccountViewSet)
router.register(r"destinations", DestinationViewSet)
router.register(r"account_members", AccountMemberViewSet)

urlpatterns = [
    path("auth/signup/", user_signup, name="signup"),
    path("auth/login/", user_login, name="login"),
    path("auth/logout/", user_logout, name="logout"),

    path("", include(router.urls)),

    path("accounts/<uuid:account_id>/destinations/", get_account_destinations, name="account_destinations"),
    path("accounts/<uuid:account_id>/logs/", get_logs, name="get_logs"),

    path("server/incoming_data/", incoming_data, name="incoming_data"),
]
