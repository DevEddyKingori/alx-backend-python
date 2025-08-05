import logging
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden, JsonResponse
import time
from collections import defaultdict

class RequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('request_logger')
        handler = logging.FileHandler('requests.log')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().hour
        # Allow access only between 18 (6PM) and 21 (9PM) inclusive
        if not (18 <= now <= 21):
            return HttpResponseForbidden('Access to messaging app is restricted during these hours.')
        return self.get_response(request)

class OffensiveLanguageMiddleware(MiddlewareMixin):
    message_limit = 5
    time_window = 60  # seconds
    ip_message_times = defaultdict(list)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST':
            ip = request.META.get('REMOTE_ADDR', 'unknown')
            now = time.time()
            # Remove timestamps older than time_window
            self.ip_message_times[ip] = [t for t in self.ip_message_times[ip] if now - t < self.time_window]
            if len(self.ip_message_times[ip]) >= self.message_limit:
                return JsonResponse({'error': 'Message limit exceeded. Try again later.'}, status=429)
            self.ip_message_times[ip].append(now)
        return self.get_response(request)

class RolepermissionMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)
        # Check for admin or moderator role
        if not (user and user.is_authenticated and (getattr(user, 'is_superuser', False) or getattr(user, 'is_staff', False) or getattr(user, 'role', None) in ['admin', 'moderator'])):
            return HttpResponseForbidden('You do not have permission to perform this action.')
        return self.get_response(request)