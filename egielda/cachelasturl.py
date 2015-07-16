from django.conf import settings


class CacheLastURLMiddleware:
    def process_request(self, request):
        settings.CURRENT_URL = request.build_absolute_uri()
