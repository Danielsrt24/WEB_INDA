from django.conf import settings
from django.shortcuts import redirect


class RedirectNotFoundToDefaultPageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        accept = request.headers.get('Accept', '')
        is_html_request = 'text/html' in accept
        static_prefix = '/' + settings.STATIC_URL.lstrip('/')
        media_prefix = '/' + settings.MEDIA_URL.lstrip('/')
        is_static_or_media = request.path.startswith(
            (static_prefix, media_prefix)
        )

        if response.status_code != 404 or not is_html_request or is_static_or_media:
            return response

        return redirect('/')
