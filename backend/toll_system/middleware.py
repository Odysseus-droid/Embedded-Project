from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class DisableCsrfOnApiMiddleware(MiddlewareMixin):
    """
    Globally disables CSRF protection for any API endpoint.
    Checks if the request path starts with the API prefix.
    """
    def process_request(self, request):
        # Check if the request path starts with the API base URL (e.g., '/api/')
        if request.path.startswith('/api/'):
            # This flag tells Django's CsrfViewMiddleware that processing is done, 
            # effectively exempting the request from the CSRF check.
            request.csrf_processing_done = True
        return None