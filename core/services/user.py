import logging
from datetime import datetime

from django.contrib.auth import get_user_model, hashers
from django.utils.translation import gettext as _
from django_core import exceptions
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt import tokens

from core.apps.accounts.choices import AuthProviderChoice
from core.services import sms


class UserService(sms.SmsService):
    def get_token(self, user):
        refresh = tokens.RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def create_user(self, phone, first_name, last_name, password, provider=None):
        if provider is None:
            provider = AuthProviderChoice.PHONE
        return get_user_model().objects.update_or_create(
            phone=phone,
            auth_provider=provider,
            defaults={
                "phone": phone,
                "first_name": first_name,
                "last_name": last_name,
                "password": hashers.make_password(password),
            },
        )

    def send_confirmation(self, phone) -> bool:
        try:
            self.send_confirm(phone)
            return True
        except exceptions.SmsException as e:
            raise PermissionDenied(_("Qayta sms yuborish uchun kuting: {}").format(e.kwargs.get("expired")))
        except Exception as e:
            logging.error(e)
            raise PermissionDenied(_("Serverda xatolik yuz berdi"))

    def validate_user(self, user) -> dict:
        """
        Create user if user not found
        """
        if user.validated_at is None:
            user.validated_at = datetime.now()
        user.save()
        token = self.get_token(user)
        return token

    def is_validated(self, user) -> bool:
        """
        User is validated check
        """
        if user.validated_at is not None:
            return True
        return False

    def change_password(self, phone, password):
        """
        Change password
        """
        user = get_user_model().objects.filter(phone=phone).first()
        user.set_password(password)
        user.save()
