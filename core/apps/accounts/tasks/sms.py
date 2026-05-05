#type: ignore
"""
Base celery tasks
"""

import logging
import os
from importlib import import_module

from celery import shared_task
from config.env import env
from django.utils.translation import gettext as _


@shared_task
def SendConfirm(phone, code):
    message = env.str(
        "OTP_MESSAGE",
        _("Menga qo'lingni uzat ilovasida tasdiqlash kodi: %(code)s"),
    ) % {"code": code}
    status = "sent"
    error = ""

    try:
        service = getattr(
            import_module(os.getenv("OTP_MODULE")), os.getenv("OTP_SERVICE")
        )()
        service.send_sms(phone, message)
        logging.info("Sms send: %s-%s" % (phone, code))
    except Exception as e:
        status = "failed"
        error = str(e)
        logging.error(
            "Error: {phone}-{code}\n\n{error}".format(phone=phone, code=code, error=e)
        )
    finally:
        try:
            from core.apps.accounts.models import SmsLog
            SmsLog.log(phone=phone, message=message, status=status, error=error)
        except Exception as log_err:
            logging.error("SmsLog write failed: %s" % log_err)

    if status == "failed":
        raise Exception
