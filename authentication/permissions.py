from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.views.generic.base import View
from rest_framework.permissions import BasePermission
from django.core.cache import cache
from rest_framework.request import Request

from .settings import AUTH_SIGN_UP_BY_IP_LIMIT, MAX_LOGIN_RETRIES
from .utils import get_request_ip


class CanCreateNewUser(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        """
            Check request IP to block users to create multiple users programmatically
        :param request:
        :param view:
        :return:
        """
        ip_address = get_request_ip(request)
        sign_up_tries = cache.get(f'SIGN_UP_{ip_address}', {})

        try:
            last_sign_up_try = datetime.strptime(sign_up_tries.get('last_sign_up_try', ''), '%d-%m-%Y %H:%M:%S')
            time_since_last_try = datetime.now() - last_sign_up_try

            if time_since_last_try < timedelta(hours=24) \
                    and sign_up_tries.get('tries') >= AUTH_SIGN_UP_BY_IP_LIMIT:
                return False
            elif time_since_last_try > timedelta(hours=24):
                sign_up_tries = {
                    'tries': 1,
                    'last_sign_up_try': datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
                }
                cache.set(f'SIGN_UP_{ip_address}', sign_up_tries)
                return True

        except ValueError:
            pass

        sign_up_tries = {
            'tries': sign_up_tries.get('tries', 0) + 1,
            'last_sign_up_try': datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
        }

        cache.set(f'SIGN_UP_{ip_address}', sign_up_tries)
        return True


class IsUserActive(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_active


class MaxPasswordRetries(BasePermission):
    def has_permission(self, request: Request, view: View):
        retries = cache.get(f'LOGIN_RETRIES_{request.data.get("username")}', 0)
        return retries <= MAX_LOGIN_RETRIES
