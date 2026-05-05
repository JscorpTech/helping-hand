"""
Admin panel register
"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth import models as db_models
from django_core.models import SmsConfirm

from ..admin import user
from ..models import SmsLog
from .user import SmsConfirmAdmin, SmsLogAdmin

admin.site.unregister(db_models.Group)
admin.site.register(db_models.Group, user.GroupAdmin)
admin.site.register(db_models.Permission, user.PermissionAdmin)

admin.site.register(get_user_model(), user.CustomUserAdmin)
admin.site.register(SmsConfirm, SmsConfirmAdmin)
admin.site.register(SmsLog, SmsLogAdmin)
