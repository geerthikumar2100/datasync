"""
URL configuration for datasync project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from core.views.data_handler import incoming_data

admin.site.site_header = "Broadcaster"
admin.site.site_title = "Broadcaster Portal"
admin.site.index_title = "Welcome to Broadcaster"

def redirect_based_on_user(request):
    if request.user.is_authenticated:
        return redirect('admin:index')
    return redirect('admin:login')

urlpatterns = [
    path('admin/login/', auth_views.LoginView.as_view(
        template_name='admin/login.html',
        redirect_authenticated_user=True,
        next_page='admin:index'  # Explicitly set next_page
    ), name='login'),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('server/incoming_data/', incoming_data, name='incoming_data'),
    path('', redirect_based_on_user, name='root'),
]
