from django.shortcuts import redirect
from django.urls import resolve

class NonStaffAdminMiddleware:
    """Middleware to handle non-staff user access to admin interface"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # # Skip middleware for incoming_data endpoint and API paths
        # if request.path.startswith('/server/') or request.path.startswith('/api/'):
        #     return self.get_response(request)

        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated and request.path != '/admin/login/':
                return redirect('/admin/login/')
            
            if request.user.is_authenticated:
                # Temporarily grant staff status to all authenticated users
                request.user.is_staff = True
                
        response = self.get_response(request)
        return response