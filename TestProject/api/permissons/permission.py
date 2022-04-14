import jwt
from django.conf import settings
from rest_framework.permissions import BasePermission


def check_permition(token: str) -> bool:
    try:
        result = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if result.get('role') == 'post_message_confirm':
            result = True
        else:
            result = False
    except:
        result = False
    return result

class ListenerOnly(BasePermission):
    def has_permission(self, request, view):
        token = request.META.get("HTTP_AUTHORIZATION", " ")
        return check_permition(token)
