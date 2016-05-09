from rest_framework import status


DEFAULT_MESSAGES = {
    status.HTTP_400_BAD_REQUEST: 'Validation error.',
    status.HTTP_404_NOT_FOUND: 'Not found.',
    status.HTTP_500_INTERNAL_SERVER_ERROR: 'Internal server error.',
}

DEFAULT_STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR

class Permissions(object):
    OWNER = 3700
    ADMIN = 2700
    WRITE = 1600
    READ = 1400
    GUEST_WRITE = 600
    GUEST_READ = 400
    NONE = 0
