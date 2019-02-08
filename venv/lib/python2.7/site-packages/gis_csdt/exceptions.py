from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from django import VERSION as DJANGO_VERSION


def custom_exception_handler(exc, context=None):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    if DJANGO_VERSION[0] >= 1 and DJANGO_VERSION[1] >= 7:
        response = exception_handler(exc, context)
    else:
        response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
