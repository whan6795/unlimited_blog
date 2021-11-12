from rest_framework.response import Response
from rest_framework import status


def reformat_resp(code, body, message='', http_status=status.HTTP_200_OK):
    data = {
        "code": code,
        "body": body,
        "message": message
    }
    resp = Response(data, status=http_status)
    return resp
