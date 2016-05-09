import json

from django.http import HttpResponse

from core.constants import DEFAULT_STATUS_CODE
from core.serializers import ErrorsSerializer


class APIErrorResponse(HttpResponse):
    """
    An HttpResponse that formats errors into a specific format.

    """
    status_code = DEFAULT_STATUS_CODE

    def __init__(self, error_list=None, status=None, *args, **kwargs):
        self.status_code = status or self.status_code

        errors = ErrorsSerializer({'errors': error_list})
        return super(APIErrorResponse, self).__init__(
            content=json.dumps(errors.data),
            status=self.status_code,
            content_type='application/json',
            *args,
            **kwargs
        )
