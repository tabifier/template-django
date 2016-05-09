from django.conf import settings


class RollerAPIMiddleware(object):
    def process_request(self, request):
        auth_present = any([
            'Authorization' in request.META,
            'access_token' in request.GET,
        ])
        if not auth_present and settings.API_COOKIE_NAME in request.COOKIES:
            request.META['Authorization'] = 'Bearer {}'.format(request.COOKIES.get(settings.API_COOKIE_NAME))
