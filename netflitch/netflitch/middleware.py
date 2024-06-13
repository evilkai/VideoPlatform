from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class CsrfDebugMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'POST' and 'csrftoken' not in request.COOKIES:
            print('CSRF cookie not found in request')
        return None