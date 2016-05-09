import logging
from django.conf import settings
from collections import OrderedDict

from rest_framework import status
from rest_framework.exceptions import APIException, ParseError
from rest_framework.views import exception_handler as drf_exception_handler
from core.responses import APIErrorResponse

logger = logging.getLogger(__name__)


ERROR_CODES = {
    0: u'Parse Error',
    10: u'General Error',
    20: u'Server Error',

    100: u'General Authentication Error',
    101: u'Incorrect email or password',
    110: u'Unauthorized access to a resource',

    300: u'General Validation Error',
    301: u'General Request Error',
    404: u'Resource does not exist',
}

ERROR_CODE_DETAILS = {
    0: ERROR_CODES[0],
    10: ERROR_CODES[10],
    20: ERROR_CODES[20],
    100: ERROR_CODES[100],
    101: ERROR_CODES[101],
    110: 'You don\'t have sufficent privileges to access this resource',
    300: ERROR_CODES[300],
    301: ERROR_CODES[301],
    404: ERROR_CODES[404],
}

class BaseAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, status_code=None, data=None):
        self.status_code = status_code or self.status_code
        self.data = data


class InvalidCredentialException(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    error_list = [{
        "code": 101,
        "title": ERROR_CODES[101],
        "detail": ERROR_CODE_DETAILS[101],
    }]


class NotFoundException(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    error_list = [{
        "code": 404,
        "title": ERROR_CODES[404],
        "detail": ERROR_CODE_DETAILS[404]
    }]


class UnAuthorizedAccessException(BaseAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    error_list = [{
        "code": 110,
        "title": ERROR_CODES[110],
        "detail": ERROR_CODE_DETAILS[110]
    }]


class SerializerValidationException(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST

    @property
    def error_list(self):
        error_list = []
        for item in self.data.keys():
            error = {
                "code": 300,
                "title": ERROR_CODES[300],
                "detail": ", ".join(self.data[item]),
            }
            if item != '__all__':
                error["source"] = item
            error_list.append(error)

        return error_list


class GeneralErrorException(BaseAPIException):
    """
    The data field can either be a string, list or tuple
    """
    status_code = status.HTTP_400_BAD_REQUEST

    @property
    def error_list(self):
        val = self.data
        if isinstance(self.data, str) or isinstance(self.data, unicode):
            val = [self.data]

        error_list = [{
            "code": 301,
            "title": ERROR_CODES[301],
            "detail": item,
        } for item in val]
        return error_list


class ExceptionHandler(object):
    @classmethod
    def handle_exception(cls, exc, *args, **kwargs):
        """
        Typically the exception will have enough data to represent itself (i.e. status_code, message).
        Otherwise we'll have to map the exception to a local exception in EXCEPTION_MAPPING.

        """
        if isinstance(exc, BaseAPIException):
            logger.warning('Encountered APIError when processing api request.', exc_info=True)
            return APIErrorResponse(
                status=exc.status_code,
                error_list=exc.error_list
            )
        elif isinstance(exc, ParseError):
            return APIErrorResponse(
                error_list=[{"code": 0, "title": ERROR_CODES[0], "detail": exc.detail}],
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            # exception wasnt a custom `APIError` fallback to DRF exception handling
            response = drf_exception_handler(exc, *args, **kwargs)

            if response:
                logger.warning('Encountered DRF exception when processing api request.', exc_info=True)
                # need to format DRF error response to our style of error response
                # as DRF may have added headers and other details to the response

                return APIErrorResponse(
                    error_list=[OrderedDict(
                        code=10,
                        title=ERROR_CODES[10],
                        detail=response.data.pop('detail'),
                    )],
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                logger.error('Encountered an unhandleded api exception when processing api request.', exc_info=True)
                if not settings.DEBUG:
                    return APIErrorResponse(
                        error_list=[OrderedDict(
                            code=20,
                            title=ERROR_CODES[20],
                            detail=(
                                'An unexpted error has occured while processing your request, our engineers have been altered. '
                                'You can also contact our support if this error is blocking you.'),
                        )],
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )
            # fallback to django exception handling
            logger.warning('Encountered an unhandled exception when processing api request.')
            return None


api_exception_handler = ExceptionHandler.handle_exception
