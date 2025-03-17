from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views.auth_views import user_signup, user_login, user_logout
from core.views.api_views import AccountViewSet, DestinationViewSet, AccountMemberViewSet, get_account_destinations, get_logs
from core.views.data_handler import incoming_data
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r"accounts", AccountViewSet)
router.register(r"destinations", DestinationViewSet)
router.register(r"account_members", AccountMemberViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Broadcaster API",
        default_version='v1',
        description="API documentation for Broadcaster System",
        terms_of_service="https://www.broadcaster.com/terms/",
        contact=openapi.Contact(email="contact@broadcaster.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Prefix all API routes with 'api/'
    path('api/', include([
        path('auth/signup/', user_signup, name="signup"),
        path('auth/login/', user_login, name="login"),
        path('auth/logout/', user_logout, name="logout"),
        
        path('accounts/<uuid:account_id>/destinations/', get_account_destinations, name="account_destinations"),
        path('accounts/<uuid:account_id>/logs/', get_logs, name="get_logs"),
        
        path('server/incoming_data/', incoming_data, name="incoming_data"),
        
        # Include router URLs
        path('', include(router.urls)),
        
        # Swagger URLs
        path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ])),
]
